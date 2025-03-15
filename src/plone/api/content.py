"""Module that provides functionality for content manipulation."""

from Acquisition import aq_chain
from Acquisition import aq_inner
from copy import copy as _copy
from itertools import islice
from plone.api import portal
from plone.api.exc import InvalidParameterError
from plone.api.validation import at_least_one_of
from plone.api.validation import mutually_exclusive_parameters
from plone.api.validation import required_parameters
from plone.app.linkintegrity.exceptions import LinkIntegrityNotificationException
from plone.app.uuid.utils import uuidToObject
from plone.uuid.interfaces import IUUID
from Products.CMFCore.DynamicType import DynamicType
from Products.CMFCore.WorkflowCore import WorkflowException
from zope.component import ComponentLookupError
from zope.component import getMultiAdapter
from zope.component import getSiteManager
from zope.container.interfaces import INameChooser
from zope.globalrequest import getRequest
from zope.interface import Interface
from zope.interface import providedBy

import transaction
import uuid


_marker = []

# Maximum number of attempts to generate a unique random ID
MAX_UNIQUE_ID_ATTEMPTS = 100


@required_parameters("container", "type")
@at_least_one_of("id", "title")
def create(
    container=None,
    type=None,
    id=None,
    title=None,
    safe_id=False,
    **kwargs,  # NOQA: C816, S101
):
    """Create a new content item.

    :param container: [required] Container object in which to create the new
        object.
    :type container: Folderish content object
    :param type: [required] Type of the object.
    :type type: string
    :param id: Id of the object.  If the id conflicts with another object in
        the container, a suffix will be added to the new object's id. If no id
        is provided, automatically generate one from the title. If there is no
        id or title provided, raise a ValueError.
    :type id: string
    :param title: Title of the object. If no title is provided, use id as
        the title.
    :type title: string
    :param safe_id: When False, the given id will be enforced. If the id is
        conflicting with another object in the target container, raise an
        InvalidParameterError. When True, choose a new, non-conflicting id.
    :type safe_id: boolean

    :returns: Content object
    :raises:
        KeyError,
        :class:`~plone.api.exc.MissingParameterError`,
        :class:`~plone.api.exc.InvalidParameterError`
    :Example: :ref:`content-create-example`
    """
    # Create a temporary id if the id is not given
    if not safe_id and id:
        content_id = id
    else:
        # Try to generate a unique random ID using UUID4
        attempts = 0
        while attempts < MAX_UNIQUE_ID_ATTEMPTS:
            content_id = str(uuid.uuid4())
            if content_id not in container:
                break
            attempts += 1
        # If we couldn't find a unique ID after max attempts, raise ValueError
        if attempts >= MAX_UNIQUE_ID_ATTEMPTS:
            raise ValueError("Could not find unique id while creating content.")

    if title:
        kwargs["title"] = title

    try:
        container.invokeFactory(type, content_id, **kwargs)
    except UnicodeDecodeError:
        # UnicodeDecodeError is a subclass of ValueError,
        # so will be swallowed below unless we re-raise it here
        raise
    except ValueError as e:
        types = [fti.getId() for fti in container.allowedContentTypes()]

        raise InvalidParameterError(
            "Cannot add a '{obj_type}' object with id={obj_id} to the container {container_path}.\n"
            "Allowed types are:\n"
            "{allowed_types}\n"
            "{message}".format(
                obj_type=type,
                obj_id=content_id,
                container_path="/".join(container.getPhysicalPath()),
                allowed_types="\n".join(sorted(types)),
                message=str(e),
            ),
        )

    content = container[content_id]
    if not id or (safe_id and id):
        # Create a new id from title
        chooser = INameChooser(container)
        derived_id = id or title
        new_id = chooser.chooseName(derived_id, content)
        # kacee: we must do a partial commit, else the renaming fails because
        # the object isn't in the zodb.
        # Thus if it is not in zodb, there's nothing to move. We should
        # choose a correct id when
        # the object is created.
        # maurits: tests run fine without this though.
        transaction.savepoint(optimistic=True)
        content.aq_parent.manage_renameObject(content_id, new_id)

    return content


@mutually_exclusive_parameters("path", "UID")
@at_least_one_of("path", "UID")
def get(path=None, UID=None):
    """Get an object.

    :param path: Path to the object we want to get, relative to
        the portal root.
    :type path: string
    :param UID: UID of the object we want to get.
    :type UID: string
    :returns: Content object
    :raises:
        ValueError,
    :Example: :ref:`content-get-example`
    """
    if path:
        site = portal.get()
        site_absolute_path = "/".join(site.getPhysicalPath())
        if not path.startswith(f"{site_absolute_path}"):
            path = "{site_path}{relative_path}".format(
                site_path=site_absolute_path,
                relative_path=path,
            )
        try:
            path = path.split("/")
            if len(path) > 1:
                parent = site.unrestrictedTraverse(path[:-1])
                content = parent.restrictedTraverse(path[-1])
            else:
                content = site.restrictedTraverse(path[-1])
        except (KeyError, AttributeError):
            return None  # When no object is found don't raise an error
        else:
            # Only return a content if it implements DynamicType,
            # which is true for Dexterity content and Comment (plone.app.discussion)
            return content if isinstance(content, DynamicType) else None

    elif UID:
        return uuidToObject(UID)


@required_parameters("source")
@at_least_one_of("target", "id")
def move(source=None, target=None, id=None, safe_id=False):
    """Move the object to the target container.

    :param source: [required] Object that we want to move.
    :type source: Content object
    :param target: Target container to which the source object will
        be moved. If no target is specified, the source object's container will
        be used as a target, effectively making this operation a rename
        (:ref:`content-rename-example`).
    :type target: Folderish content object
    :param id: Pass this parameter if you want to change the id of the moved
        object on the target location. If the new id conflicts with another
        object in the target container, a suffix will be added to the moved
        object's id.
    :type id: string
    :param safe_id: When False, the given id will be enforced. If the id is
        conflicting with another object in the target container, raise a
        InvalidParameterError. When True, choose a new, non-conflicting id.
    :type safe_id: boolean
    :returns: Content object that was moved to the target location
    :raises:
        KeyError
        ValueError
    :Example: :ref:`content-move-example`
    """
    source_id = source.getId()

    # If no target is given the object is probably renamed
    if target and source.aq_parent is not target:
        target.manage_pasteObjects(
            source.aq_parent.manage_cutObjects(source_id),
        )
    else:
        target = source.aq_parent

    if id:
        return rename(obj=target[source_id], new_id=id, safe_id=safe_id)
    else:
        return target[source_id]


@required_parameters("obj", "new_id")
def rename(obj=None, new_id=None, safe_id=False):
    """Rename the object.

    :param obj: [required] Object that we want to rename.
    :type obj: Content object
    :param new_id: New id of the object.
    :type new_id: string
    :param safe_id: When False, the given id will be enforced. If the id is
        conflicting with another object in the container, raise a
        InvalidParameterError. When True, choose a new, non-conflicting id.
    :type safe_id: boolean
    :returns: Content object that was renamed
    :Example: :ref:`content-rename-example`
    """
    obj_id = obj.getId()
    container = obj.aq_parent

    if safe_id:
        chooser = INameChooser(container)
        new_id = chooser.chooseName(new_id, obj)

    if obj_id != new_id:
        container.manage_renameObject(obj_id, new_id)
    return container[new_id]


@required_parameters("source")
@at_least_one_of("target", "id")
def copy(source=None, target=None, id=None, safe_id=False):
    """Copy the object to the target container.

    :param source: [required] Object that we want to copy.
    :type source: Content object
    :param target: Target container to which the source object will
        be moved. If no target is specified, the source object's container will
        be used as a target.
    :type target: Folderish content object
    :param id: Id of the copied object on the target location. If no id is
        provided, the copied object will have the same id as the source object
        - however, if the new object's id conflicts with another object in the
        target container, a suffix will be added to the new object's id.
    :type id: string
    :param safe_id: When False, the given id will be enforced. If the id is
        conflicting with another object in the target container, raise a
        InvalidParameterError. When True, choose a new, non-conflicting id.
    :type safe_id: boolean
    :returns: Content object that was created in the target location
    :raises:
        KeyError,
        ValueError
    :Example: :ref:`content-copy-example`
    """
    source_id = source.getId()

    if target is None:
        target = source.aq_parent

    copy_info = target.manage_pasteObjects(
        source.aq_parent.manage_copyObjects(source_id),
    )

    new_id = copy_info[0]["new_id"]
    if id:
        if not safe_id and id in target:
            msg = "Duplicate ID '{0}' in '{1}' for '{2}'"
            raise InvalidParameterError(msg.format(id, target, source))
        else:
            return rename(obj=target[new_id], new_id=id, safe_id=safe_id)
    else:
        return target[new_id]


@mutually_exclusive_parameters("obj", "objects")
@at_least_one_of("obj", "objects")
def delete(obj=None, objects=None, check_linkintegrity=True):
    """Delete the object(s).

    :param obj: Object that we want to delete.
    :type obj: Content object
    :param objects: Objects that we want to delete.
    :type objects: List of content objects
    :param check_linkintegrity: Raise exception if there are
        linkintegrity-breaches.
    :type check_linkintegrity: boolean

    :raises:
        ValueError
        plone.app.linkintegrity.exceptions.LinkIntegrityNotificationException

    :Example: :ref:`content-delete-example`
    """
    objects = [obj] if obj else objects

    # Return early if we have no objects to delete.
    if not objects:
        return

    if check_linkintegrity:
        site = portal.get()
        linkintegrity_view = get_view(
            name="delete_confirmation_info",
            context=site,
            request=site.REQUEST,
        )
        # look for breaches and manually raise a exception
        breaches = linkintegrity_view.get_breaches(objects)
        if breaches:
            raise LinkIntegrityNotificationException(
                f"Linkintegrity-breaches: {breaches}",
            )

    for obj_ in objects:
        obj_.aq_parent.manage_delObjects([obj_.getId()])


@required_parameters("obj")
def get_state(obj=None, default=_marker):
    """Get the current workflow state of the object.

    :param obj: [required] Object that we want to get the state for.
    :type obj: Content object
    :param default: Returned if no workflow is defined for the object.
    :returns: Object's current workflow state, or `default`.
    :rtype: string
    :raises:
        Products.CMFCore.WorkflowCore.WorkflowException
    :Example: :ref:`content-get-state-example`
    """
    workflow = portal.get_tool("portal_workflow")

    if default is not _marker and not workflow.getWorkflowsFor(obj):
        return default

    # This still raises WorkflowException when the workflow state is broken,
    # ie 'review_state' is absent
    return workflow.getInfoFor(ob=obj, name="review_state")


# work backwards from our end state
def _find_path(maps, path, current_state, start_state):
    paths = []
    # current_state could not be on maps if it only has outgoing
    # transitions. i.e an initial state you are not able to return to.
    if current_state not in maps:
        return

    for new_transition, from_states in maps[current_state]:
        next_path = _copy(path)
        if new_transition in path:
            # Don't go in a circle
            continue

        next_path.insert(0, new_transition)
        if start_state in from_states:
            paths.append(next_path)
            continue

        for state in from_states:
            recursive_paths = _find_path(
                maps,
                next_path,
                state,
                start_state,
            )
            if recursive_paths:
                paths.append(recursive_paths)

    return len(paths) and min(paths, key=len) or None


def _wf_transitions_for(workflow, from_state, to_state):
    """Get list of transition IDs required to transition.

    from ``from_state`` to ``to_state``.

    :param workflow: Workflow object which contains states and transitions
    :type workflow: Workflow object
    :param from_state: Current workflow state
    :type from_state: string
    :param to_state: Desired workflow state
    :type to_state: string
    :returns: A list of transitions
    :rtype: list
    """
    exit_state_maps = {}
    for state in workflow.states.objectValues():
        for transition in state.getTransitions():
            exit_state_maps.setdefault(transition, [])
            exit_state_maps[transition].append(state.getId())

    transition_maps = {}
    for transition in workflow.transitions.objectValues():
        value = (
            transition.getId(),
            exit_state_maps.get(transition.getId(), []),
        )
        if transition.new_state_id not in transition_maps:
            transition_maps[transition.new_state_id] = [value]
        else:
            transition_maps[transition.new_state_id].append(value)

    if to_state not in transition_maps:
        # impossible to reach via this workflow
        return None

    return _find_path(transition_maps, [], to_state, from_state)


def _transition_to(obj, workflow, to_state, **kwargs):
    # move from the current state to the given state
    # via any route we can find
    for wf in workflow.getWorkflowsFor(obj):
        status = workflow.getStatusOf(wf.getId(), obj)
        if not status or not status.get("review_state"):
            continue
        if status["review_state"] == to_state:
            return

        transitions = _wf_transitions_for(
            wf,
            status["review_state"],
            to_state,
        )
        if not transitions:
            continue

        for transition in transitions:
            try:
                workflow.doActionFor(obj, transition, **kwargs)
            except WorkflowException:
                # take into account automatic transitions.
                # If the transitions list that are being iterated over
                # have automatic transitions they need to be skipped
                if get_state(obj) == to_state:
                    break

        break


@required_parameters("obj")
@at_least_one_of("transition", "to_state")
@mutually_exclusive_parameters("transition", "to_state")
def transition(obj=None, transition=None, to_state=None, **kwargs):
    """Perform a workflow transition.

    for the object or attempt to perform
    workflow transitions on the object to reach the given state.
    The later will not guarantee that transition guards conditions can be met.

    Accepts kwargs to supply to the workflow policy in use, such as "comment"

    :param obj: [required] Object for which we want to perform the workflow
        transition.
    :type obj: Content object
    :param transition: Name of the workflow transition.
    :type transition: string
    :param to_state: Name of the workflow state.
    :type to_state: string
    :raises:
        :class:`~plone.api.exc.MissingParameterError`,
        :class:`~plone.api.exc.InvalidParameterError`
    :Example: :ref:`content-transition-example`
    """
    workflow = portal.get_tool("portal_workflow")
    if transition is not None:
        try:
            workflow.doActionFor(obj, transition, **kwargs)
        except WorkflowException:
            transitions = [action["id"] for action in workflow.listActions(object=obj)]

            raise InvalidParameterError(
                "Invalid transition '{}'.\n"
                "Valid transitions are:\n"
                "{}".format(transition, "\n".join(sorted(transitions))),
            )
    else:
        _transition_to(obj, workflow, to_state, **kwargs)
        if workflow.getInfoFor(obj, "review_state") != to_state:
            raise InvalidParameterError(
                "Could not find workflow to set state to {} on {}".format(
                    to_state,
                    obj,
                ),
            )


@required_parameters("obj")
def disable_roles_acquisition(obj=None):
    """Disable acquisition of local roles on given obj.

    Set __ac_local_roles_block__ = 1 on obj.

    :param obj: [required] Context object to block the acquisition on.
    :type obj: Content object
    :Example: :ref:`content-disable-roles-acquisition-example`
    """
    plone_utils = portal.get_tool("plone_utils")
    plone_utils.acquireLocalRoles(obj, status=0)


@required_parameters("obj")
def enable_roles_acquisition(obj=None):
    """Enable acquisition of local roles on given obj.

    Set __ac_local_roles_block__ = 0 on obj.

    :param obj: [required] Context object to enable the acquisition on.
    :type obj: Content object
    :Example: :ref:`content-enable-roles-acquisition-example`
    """
    plone_utils = portal.get_tool("plone_utils")
    plone_utils.acquireLocalRoles(obj, status=1)


@required_parameters("name", "context")
def get_view(name=None, context=None, request=None):
    """Get a BrowserView object.

    :param name: [required] Name of the view.
    :type name: string
    :param context: [required] Context on which to get view.
    :type context: context object
    :param request: [required] Request on which to get view.
    :type request: request object
    :raises:
        :class:`~plone.api.exc.MissingParameterError`,
        :class:`~plone.api.exc.InvalidParameterError`
    :Example: :ref:`content-get-view-example`
    """
    if request is None:
        request = getRequest()
    # We do not use exceptionhandling to detect if the requested view is
    # available, because the __init__ of said view will contain
    # errors in client code.

    try:
        return getMultiAdapter((context, request), name=name)
    except ComponentLookupError:
        # Getting all available views
        sm = getSiteManager()
        available_views = sm.adapters.lookupAll(
            required=(providedBy(context), providedBy(request)),
            provided=Interface,
        )

        # Check if the requested view is available
        # by getting the names of all available views
        available_view_names = [view[0] for view in available_views]
        if name not in available_view_names:
            # Raise an error if the requested view is not available.
            raise InvalidParameterError(
                "Cannot find a view with name '{name}'.\n"
                "Available views are:\n"
                "{views}".format(
                    name=name,
                    views="\n".join(sorted(available_view_names)),
                ),
            )


@required_parameters("obj")
def get_uuid(obj=None):
    """Get the object's Universally Unique IDentifier (UUID).

    :param obj: [required] Object we want its UUID.
    :type obj: Content object
    :returns: Object's UUID
    :rtype: string
    :raises:
        ValueError
    :Example: :ref:`content-get-uuid-example`
    """
    return IUUID(obj)


@required_parameters("obj")
def get_path(obj=None, relative=False):
    """Get the path of an object.

    :param obj: [required] Object for which to get its path
    :type obj: Content object
    :param relative: Return a relative path from the portal root
    :type relative: boolean
    :returns: Path to the object
    :rtype: string
    :raises:
        InvalidParameterError
    :Example: :ref:`content-get-path-example`
    """
    if not hasattr(obj, "getPhysicalPath"):
        raise InvalidParameterError(f"Cannot get path of object {obj!r}")

    if not relative:
        return "/".join(obj.getPhysicalPath())
    site = portal.get()
    site_path = site.getPhysicalPath()
    obj_path = obj.getPhysicalPath()
    if obj_path[: len(site_path)] != site_path:
        raise InvalidParameterError(
            "Object not in portal path. Object path: {}".format("/".join(obj_path))
        )
    rel_path = obj_path[len(site_path) :]
    return "/".join(rel_path) if rel_path else ""


def _parse_object_provides_query(query):
    """Create a query for the object_provides index.

    :param query: [required]
    :type query: Single (or list of) Interface or Identifier or a KeywordIndex
        query for multiple values
        (eg. `{'query': [Iface1, Iface2], 'operator': 'or'}`)
    """
    ifaces = query
    operator = "or"
    query_not = []

    if isinstance(query, dict):
        ifaces = query.get("query", [])
        operator = query.get("operator", operator)
        query_not = query.get("not", [])
        # KeywordIndex also supports "range",
        # but that's not useful for querying object_provides

    if not isinstance(ifaces, (list, tuple)):
        ifaces = [ifaces]
    ifaces = [getattr(x, "__identifier__", x) for x in ifaces]

    if not isinstance(query_not, (list, tuple)):
        query_not = [query_not]
    query_not = [getattr(x, "__identifier__", x) for x in query_not]

    result = {}

    if ifaces:
        result["query"] = ifaces
        result["operator"] = operator

    if query_not:
        result["not"] = query_not

    return result


def find(context=None, depth=None, unrestricted=False, **kwargs):
    """Find content in the portal.

    :param context: Context for the search
    :type obj: Content object
    :param depth: How far in the content tree we want to search from context
    :param unrestricted: Boolean, use unrestrictedSearchResults if True
    :type obj: Content object
    :returns: Catalog brains
    :rtype: List
    :Example: :ref:`content-find-example`

    """
    query = {}
    query.update(**kwargs)

    # Save the original path to maybe restore it later.
    orig_path = query.get("path")
    if isinstance(orig_path, dict):
        orig_path = orig_path.get("query")

    # Passing a context or depth overrides the existing path query,
    # for now.
    if context or depth is not None:
        # Make the path a dictionary, unless it already is.
        if not isinstance(orig_path, dict):
            query["path"] = {}

    # Limit search depth
    if depth is not None:
        # If we don't have a context, we'll assume the portal root.
        if context is None and not orig_path:
            context = portal.get()
        else:
            # Restore the original path
            query["path"]["query"] = orig_path
        query["path"]["depth"] = depth

    if context is not None:
        query["path"]["query"] = "/".join(context.getPhysicalPath())

    # Convert interfaces to their identifiers and also allow to query
    # multiple values using {'query:[], 'operator':'and|or'}
    obj_provides = query.get("object_provides", [])
    if obj_provides:
        query["object_provides"] = _parse_object_provides_query(obj_provides)

    # Make sure we don't dump the whole catalog.
    catalog = portal.get_tool("portal_catalog")
    indexes = catalog.indexes()
    valid_indexes = [index for index in query if index in indexes]
    if not valid_indexes:
        return []

    if unrestricted:
        return catalog.unrestrictedSearchResults(**query)
    else:
        return catalog(**query)


@required_parameters("obj")
def iter_ancestors(obj=None, function=None, interface=None, stop_at=_marker):
    """Iterate over the object ancestors.

    Optionally filter the ancestors:

    1. by a custom function.
    2. by interface.

    The iteration will stop by default at the portal root.
    If you want to stop at a specific object, pass it as the ``stop_at`` parameter.
    If you want to return all the matching objects in the acquisition chain, pass
    ``False`` as the value of the ``stop_at`` parameter.

    :param obj: [required] Object for which we want to iterate over the ancestors.
    :type obj: Content object
    :param function: Optional callable that takes an object and returns a boolean.
    :type function: callable
    :param interface: Optional interface that should be provided by the ancestor.
    :type interface: zope.interface.Interface
    :param stop_at: Optional object at which to stop the iteration. If ``False``
        is passed as the value, we will return all the matching objects in the
        acquisition chain
    :type stop_at: Content object or False
    :returns: Iterator of ancestor objects, from immediate to site root.
    :rtype: iterator
    :Example: :ref:`content-iter-ancestors-example`
    """
    if stop_at is _marker:
        stop_at = portal.get()

    if obj is stop_at:
        # We should iterate over the ancestors of obj but obj is also
        # the object at which we should stop checking for ancestors.
        # So we should return an empty iterator.
        #
        # This is useful if we want to have an empty iterator when checking
        # for ancestors in the portal.
        return iter(())

    chain = aq_chain(aq_inner(obj))

    if stop_at:
        try:
            end = chain.index(stop_at) + 1
        except ValueError:
            raise InvalidParameterError(
                f"The object {stop_at!r} is not in the acquisition chain of {obj!r}"
            )
    else:
        end = None

    ancestors = islice(chain, 1, end)

    if interface is not None:
        ancestors = filter(interface.providedBy, ancestors)

    if function is not None:
        ancestors = filter(function, ancestors)

    yield from ancestors


@required_parameters("obj")
def get_closest_ancestor(obj=None, function=None, interface=None, stop_at=_marker):
    """Get the closest ancestor that matches the criteria.

    See :func:`~plone.api.content.iter_ancestors` for more information on the parameters.

    :param obj: [required] Object for which we want to get the ancestor.
    :type obj: Content object
    :param function: Optional callable that takes an object and returns a boolean.
    :type function: callable
    :param interface: Optional interface that should be provided by the ancestor.
    :type interface: zope.interface.Interface
    :param stop_at: Optional object at which to stop the iteration. If ``False``
        is passed as the value, we will return all the matching objects in the
        acquisition chain
    :type stop_at: Content object or False
    :returns: Iterator of ancestor objects, from immediate to site root.
    :rtype: iterator
    :Example: :ref:`content-get-closest-ancestor-example`
    """
    return next(
        iter_ancestors(
            obj=obj, function=function, interface=interface, stop_at=stop_at
        ),
        None,
    )
