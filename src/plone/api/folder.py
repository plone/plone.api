# -*- coding: utf-8 -*-
"""Module that provides functionality for dealing with folder contents."""

from Products.CMFCore.utils import getToolByName
from plone.api.validation import required_parameters


@required_parameters('container')
def list_objects(
    container=None,
    content_filter={},
    sort_on=None,
    strict=False,
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

    return [brain.getObject() for brain in list_brains(
        container=container,
        content_filter=content_filter,
        sort_on=sort_on,
        strict=strict)]


@required_parameters('container')
def list_brains(
    container=None,
    content_filter={},
    sort_on=None,
    strict=False,
):
    """ List all content objects of the current folderish object as
        Zcatalog brains.

        Parameters: see plone.api.folder.list_objects()
    """

    catalog = getToolByName(container, 'portal_catalog')

    if strict:
        index_names = set(idx.getId() for idx in catalog.getIndexObjects())
        for k in content_filter:
            if k not in index_names:
                raise ValueError('Index {} does not exist'.format(k))

    if sort_on:
        content_filter['sort_on'] = sort_on
    content_filter['path'] = {'query': '/'.join(container.getPhysicalPath()),
                              'depth': 1}
    return catalog(**content_filter)
