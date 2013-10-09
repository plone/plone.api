# -*- coding: utf-8 -*-
"""Module that provides functionality for content manipulation."""

from Products.Archetypes.interfaces.base import IBaseObject
from Products.CMFCore.interfaces import ISiteRoot
from Products.CMFCore.WorkflowCore import WorkflowException
from plone.api import portal
from plone.api.exc import InvalidParameterError
from plone.api.validation import at_least_one_of
from plone.api.validation import mutually_exclusive_parameters
from plone.api.validation import required_parameters
from plone.app.uuid.utils import uuidToObject
from plone.uuid.interfaces import IUUID
from zope.component import getMultiAdapter
from zope.component import getSiteManager
from zope.container.interfaces import INameChooser
from zope.interface import Interface
from zope.interface import providedBy

import random
import transaction


@required_parameters('container', 'type')
@at_least_one_of('id', 'title')
def create(
    container=None,
    type=None,
    id=None,
    title=None,
    safe_id=False,
    **kwargs
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
    :Example: :ref:`content_create_example`
    """
    # Create a temporary id if the id is not given
    content_id = not safe_id and id or str(random.randint(0, 99999999))

    if title:
        kwargs['title'] = title

    try:
        container.invokeFactory(type, content_id, **kwargs)
    except ValueError, e:
        if ISiteRoot.providedBy(container):
            allowed_types = container.allowedContentTypes()
            types = [allowed_type.id for allowed_type in allowed_types]
        else:
            try:
                types = container.getLocallyAllowedTypes()
            except AttributeError:
                raise InvalidParameterError(
                    "Cannot add a '%s' object to the container." % type
                )

        raise InvalidParameterError(
            "Cannot add a '{0}' object to the container.\n"
            "Allowed types are:\n"
            "{1}\n"
            "{2}".format(type, '\n'.join(sorted(types)), e.message)
        )

    content = container[content_id]

    # Archetypes specific code
    if IBaseObject.providedBy(content):
        # Will finish Archetypes content item creation process,
        # rename-after-creation and such
        content.processForm()

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


@mutually_exclusive_parameters('path', 'UID')
@at_least_one_of('path', 'UID')
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
    :Example: :ref:`content_get_example`
    """
    if path:
        site = portal.get()
        site_absolute_path = site.absolute_url_path()
        if not path.startswith('{0}'.format(site_absolute_path)):
            path = '{0}{1}'.format(site_absolute_path, path)

        try:
            return site.restrictedTraverse(path)
        except KeyError:
            return None  # When no object is found don't raise an error

    elif UID:
        return uuidToObject(UID)


@required_parameters('source')
@at_least_one_of('target', 'id')
def move(source=None, target=None, id=None, safe_id=False):
    """Move the object to the target container.

    :param source: [required] Object that we want to move.
    :type source: Content object
    :param target: Target container to which the source object will
        be moved. If no target is specified, the source object's container will
        be used as a target, effectively making this operation a rename
        (:ref:`content_rename_example`).
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
    :Example: :ref:`content_move_example`
    """
    source_id = source.getId()

    # If no target is given the object is probably renamed
    if target:
        target.manage_pasteObjects(
            source.aq_parent.manage_cutObjects(source_id))
    else:
        target = source

    if id:
        return rename(obj=target[source_id], new_id=id, safe_id=safe_id)
    else:
        return target[source_id]


@required_parameters('obj', 'new_id')
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
    :Example: :ref:`content_rename_example`
    """
    obj_id = obj.getId()

    if safe_id:
        try:
            chooser = INameChooser(obj)
        except TypeError:
            chooser = INameChooser(obj.aq_parent)
        new_id = chooser.chooseName(new_id, obj)

    obj.aq_parent.manage_renameObject(obj_id, new_id)
    return obj.aq_parent[new_id]


@required_parameters('source')
@at_least_one_of('target', 'id')
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
    :param safe_id: When True, the given id will be enforced. If the id is
        conflicting with another object in the target container, raise a
        InvalidParameterError. When True, choose a new, non-conflicting id.
    :type safe_id: boolean
    :returns: Content object that was created in the target location
    :raises:
        KeyError,
        ValueError
    :Example: :ref:`content_copy_example`
    """
    source_id = source.getId()

    if target is None:
        target = source.aq_parent

    target.manage_pasteObjects(source.aq_parent.manage_copyObjects(source_id))

    if id:
        return rename(obj=target[source_id], new_id=id, safe_id=safe_id)
    else:
        return target[source_id]


@required_parameters('obj')
def delete(obj=None):
    """Delete the object.

    :param obj: [required] Object that we want to delete.
    :type obj: Content object
    :raises:
        ValueError
    :Example: :ref:`content_delete_example`
    """
    obj.aq_parent.manage_delObjects([obj.getId()])


@required_parameters('obj')
def get_state(obj=None):
    """Get the current workflow state of the object.

    :param obj: [required] Object that we want to get the state for.
    :type obj: Content object
    :returns: Object's current workflow state
    :rtype: string
    :raises:
        ValueError
    :Example: :ref:`content_get_state_example`
    """
    workflow = portal.get_tool('portal_workflow')
    return workflow.getInfoFor(obj, 'review_state')


@required_parameters('obj', 'transition')
def transition(obj=None, transition=None):
    """Perform a workflow transition for the object.

    :param obj: [required] Object for which we want to perform the workflow
        transition.
    :type obj: Content object
    :param transition: [required] Name of the workflow transition.
    :type transition: string
    :raises:
        :class:`~plone.api.exc.MissingParameterError`,
        :class:`~plone.api.exc.InvalidParameterError`
    :Example: :ref:`content_transition_example`
    """
    workflow = portal.get_tool('portal_workflow')
    try:
        workflow.doActionFor(obj, transition)
    except WorkflowException:
        transitions = [
            action['id'] for action in workflow.listActions(object=obj)
        ]

        raise InvalidParameterError(
            "Invalid transition '{0}'.\n"
            "Valid transitions are:\n"
            "{1}".format(transition, '\n'.join(sorted(transitions)))
        )


@required_parameters('name', 'context', 'request')
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
    :Example: :ref:`content_get_view_example`
    """

    try:
        return getMultiAdapter((context, request), name=name)
    except:
        # get a list of all views so we can display their names in the error
        # msg
        sm = getSiteManager()
        views = sm.adapters.lookupAll(
            required=(providedBy(context), providedBy(request)),
            provided=Interface,
        )
        views_names = [view[0] for view in views]

        raise InvalidParameterError(
            "Cannot find a view with name '{0}'.\n"
            "Available views are:\n"
            "{1}".format(name, '\n'.join(sorted(views_names)))
        )


@required_parameters('obj')
def get_uuid(obj=None):
    """Get the object's Universally Unique IDentifier (UUID).

    :param obj: [required] Object we want its UUID.
    :type obj: Content object
    :returns: Object's UUID
    :rtype: string
    :raises:
        ValueError
    :Example: :ref:`content_get_uuid_example`
    """
    return IUUID(obj)
