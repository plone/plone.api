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
    :param content_filter: ZCatalog query filter
    :type type: dict
    :param sort_on: Id of a Zcatalog metadata used for sorting the content
        objects.
    :type id: string
    :param strict: Perform a consistency check of the content_filter keys
        against the list of existing index names. Set this parameter to
        True during development or for debugging reasons because the
        additional checks take some additional time.
    :type title: bool
    :returns: list of content objects
    :raises:
        ValueError,
        :class:`~plone.api.exc.MissingParameterError`,
        :class:`~plone.api.exc.InvalidParameterError`
    :Example: :ref:`list_objects_example`
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
    """ Same as list_objects() but it returns a list of ZCatalog brains
    instead of full content objects.

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
