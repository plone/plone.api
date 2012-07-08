from Products.Archetypes.interfaces.base import IBaseObject
from zope.app.container.interfaces import INameChooser

import random


def create(container=None, type=None, id=None, title=None, strict=True, *args,
           **kwargs):
    """Create a new object.

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
    :param strict: When True, the given id will be enforced. If the id is
        conflicting with another object in the target container, raise a
        KeyError. When False, ``create`` creates a new, non-conflicting id.
    :type param: boolean
    :returns: Content object
    :Example: :ref:`create_content_example`
    """
    if not container:
        raise ValueError('The ``container`` attribute is required.')

    if not type:
        raise ValueError('The ``type`` attribute is required.')

    if not id and not title:
        raise ValueError('You have to provide either the ``id`` or the '
                         '``title`` attribute')

    # Create a temporary id
    id = str(random.randint(0, 99999999))
    container.invokeFactory(type, id, title=title, **kwargs)
    content = container[id]

    # Archetypes specific code
    if IBaseObject.providedBy(content):
        # Will finish Archetypes content item creation process,
        # rename-after-creation and such
        content.processForm()

    # Create a new id from title
    chooser = INameChooser(container)
    new_id = chooser.chooseName(title, content)
    content.aq_parent.manage_renameObject(id, new_id)

    return content


def get(path=None, UID=None, *args):
    """Get an object.

    :param path: Path to the object we want to get, relative to the site root.
    :type path: string
    :param UID: UID of the object we want to get.
    :type UID: string
    :returns: Content object
    :Example: :ref:`get_content_example`
    """
    if args:
        raise ValueError('Positional arguments are not allowed!')

    if not path or not UID:
        raise ValueError

    if path and UID:
        raise ValueError

    pass


def move(source=None, target=None, id=None, strict=False, *args):
    """Move the object to the target container.

    :param source: [required] Object that we want to move.
    :type source: Content object
    :param target: Target container to which the source object will
        be moved. If no target is specified, the source object's container will
        be used as a target, effectively making this operation a rename
        (:ref:`rename_content_example`).
    :type target: Folderish content object
    :param id: Pass this parameter if you want to change the id of the moved
        object on the target location. If the new id conflicts with another
        object in the target container, a suffix will be added to the moved
        object's id.
    :type id: string
    :param strict: When True, the given id will be enforced. If the id is
        conflicting with another object in the target container, raise a
        KeyError. When False, move creates a new, non-conflicting id.
    :type param: boolean
    :Example: :ref:`move_content_example`
    """
    if args:
        raise ValueError('Positional arguments are not allowed!')

    if not source:
        raise ValueError

    if not target and not id:
        raise ValueError

    pass


def copy(source=None, target=None, id=None, strict=False, *args):
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
    :param strict: When True, the given id will be enforced. If the id is
        conflicting with another object in the target container, raise a
        KeyError. When False, ``copy`` creates a new, non-conflicting id.
    :type param: boolean
    :Example: :ref:`copy_content_example`
    """
    if args:
        raise ValueError('Positional arguments are not allowed!')

    if not source:
        raise ValueError

    pass


def delete(obj=None, *args):
    """Delete the object.

    :param obj: [required] Object that we want to delete.
    :type obj: Content object
    :Example: :ref:`delete_content_example`
    """
    if args:
        raise ValueError('Positional arguments are not allowed!')

    if not obj:
        raise ValueError

    pass


def get_state(obj=None, *args):
    """Get the current workflow state of the object.

    :param obj: [required] Object that we want to get the state for.
    :type obj: Content object
    :returns: Object's current workflow state
    :rtype: string
    :Example: :ref:`get_state_example`
    """
    if args:
        raise ValueError('Positional arguments are not allowed!')

    if not obj:
        raise ValueError

    pass


def transition(obj=None, transition=None, *args):
    """Perform a workflow transition for the object.

    :param obj: [required] Object for which we want to perform the workflow
        transition.
    :type obj: Content object
    :param transition: [required] Name of the workflow transition.
    :type transition: string
    :Example: :ref:`transition_example`
    """
    if args:
        raise ValueError('Positional arguments are not allowed!')

    if not obj or not transition:
        raise ValueError

    pass
