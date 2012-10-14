# -*- coding: utf-8 -*-
"""Module that provides functionality for content manipulation."""

from App.config import getConfiguration
from plone.api import portal
from plone.api.exc import InvalidParameterError
from plone.api.exc import MissingParameterError
from plone.app.uuid.utils import uuidToObject
from plone.uuid.interfaces import IUUID
from Products.Archetypes.interfaces.base import IBaseObject
from Products.CMFCore.interfaces import ISiteRoot
from Products.CMFCore.WorkflowCore import WorkflowException
from Products.CMFPlone.utils import getToolByName
from zope.app.container.interfaces import INameChooser
from zope.component import getMultiAdapter
from zope.component import getSiteManager
from zope.interface import Interface
from zope.interface import providedBy

import random
import transaction


def create(container=None,
           type=None,
           id=None,
           title=None,
           safe_id=False,
           **kwargs):
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
        conflicting with another object in the target container, raise a
        InvalidParameterError. When True, choose a new, non-conflicting id.
    :type safe_id: boolean
    :returns: Content object
    :raises:
        KeyError,
        :class:`~plone.api.exc.MissingParameterError`,
        :class:`~plone.api.exc.InvalidParameterError`
    :Example: :ref:`content_create_example`

    """
    if not container:
        raise MissingParameterError("Missing required parameter: container")

    if not type:
        raise MissingParameterError("Missing required parameter: type")

    if not id and not title:
        raise MissingParameterError('You have to provide either the ``id`` or the '
                                    '``title`` parameter')

    # Create a temporary id if the id is not given
    content_id = not safe_id and id or str(random.randint(0, 99999999))

    if title:
        kwargs['title'] = title

    try:
        container.invokeFactory(type, content_id, **kwargs)
    except ValueError:
        if ISiteRoot.providedBy(container):
            types = [type.id for type in container.allowedContentTypes()]
        else:
            types = container.getLocallyAllowedTypes()

        raise InvalidParameterError(
            "Cannot add a '%s' object to the container. \n"
            "Allowed types are:\n"
            "%s" % (type, '\n'.join(sorted(types))))

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
    if path and UID:
        raise ValueError('When getting an object combining path and UID '
                         'attribute is not allowed')

    if not path and not UID:
        raise ValueError('When getting an object path or UID attribute is '
                         'required')

    if path:
        site = portal.get()
        site_id = site.getId()
        if not path.startswith('/{0}'.format(site_id)):
            path = '/{0}{1}'.format(site_id, path)

        try:
            return site.restrictedTraverse(path)
        except KeyError:
            return None  # When no object is found don't raise an error

    elif UID:
        return uuidToObject(UID)


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
    :raises:
        KeyError
        ValueError
    :Example: :ref:`content_move_example`

    """
    if not source:
        raise ValueError

    if not target and not id:
        raise ValueError

    source_id = source.getId()

    # If no target is given the object is probably renamed
    if target:
        target.manage_pasteObjects(source.manage_cutObjects(source_id))
    else:
        target = source

    if id:
        if not safe_id:
            new_id = id
        else:
            try:
                chooser = INameChooser(target)
            except TypeError:
                chooser = INameChooser(target.aq_parent)
            new_id = chooser.chooseName(id, source)

        target.manage_renameObject(source_id, new_id)


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
    :Example: :ref:`content_rename_example`

    """
    if not obj:
        raise MissingParameterError("Missing required parameter: obj")

    if not new_id:
        raise MissingParameterError("Missing required parameter: new_id")

    move(source=obj, id=new_id, safe_id=safe_id)


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
    :returns: Content object that was created in the target location
    :param safe_id: When True, the given id will be enforced. If the id is
        conflicting with another object in the target container, raise a
        InvalidParameterError. When True, choose a new, non-conflicting id.
    :type safe_id: boolean
    :raises:
        KeyError,
        ValueError
    :Example: :ref:`content_copy_example`

    """
    if not source:
        raise ValueError

    if not target and not id:
        raise ValueError

    source_id = source.getId()
    target.manage_pasteObjects(source.manage_copyObjects(source_id))

    if id:
        if not safe_id:
            new_id = id
        else:
            chooser = INameChooser(target)
            new_id = chooser.chooseName(id, source)

        target.manage_renameObject(source_id, new_id)


def delete(obj=None):
    """Delete the object.

    :param obj: [required] Object that we want to delete.
    :type obj: Content object
    :raises:
        ValueError
    :Example: :ref:`content_delete_example`

    """
    if not obj:
        raise ValueError

    obj.aq_parent.manage_delObjects([obj.getId()])


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
    if not obj:
        raise ValueError

    workflow = getToolByName(portal.get(), 'portal_workflow')
    return workflow.getInfoFor(obj, 'review_state')


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
    if not obj or not transition:
        raise MissingParameterError('You have to provide the ``obj`` and the '
                                    '``transition`` parameters')

    workflow = getToolByName(portal.get(), 'portal_workflow')
    try:
        workflow.doActionFor(obj, transition)
    except WorkflowException:
        transitions = [action['id'] for action in workflow.listActions(object=obj)]

        raise InvalidParameterError(
            "Invalid transition '%s'. \n"
            "Valid transitions are:\n"
            "%s" % (transition, '\n'.join(sorted(transitions))))


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
    if not name:
        raise MissingParameterError("Missing required parameter: name")

    if not context:
        raise MissingParameterError("Missing required parameter: context")

    if not request:
        raise MissingParameterError("Missing required parameter: request")

    # It happens sometimes that ACTUAL_URL is not set in tests. To be nice
    # and not throw strange errors, we set it to be the same as URL.
    # TODO: if/when we have api.env.test_mode() boolean in the future, use that
    config = getConfiguration()
    if config.dbtab.__module__ == 'plone.testing.z2':
        request['ACTUAL_URL'] = request['URL']

    try:
        return getMultiAdapter((context, request), name=name)
    except:
        # get a list of all views so we can display their names in the error msg
        sm = getSiteManager()
        views = sm.adapters.lookupAll(required=(providedBy(context), providedBy(request)),
                                      provided=Interface)
        views_names = [view[0] for view in views]

        raise InvalidParameterError(
            "Cannot find a view with name '%s'. \n"
            "Available views are:\n"
            "%s" % (name, '\n'.join(sorted(views_names))))


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
    if not obj:
        raise ValueError

    return IUUID(obj)
