""" Module that provides functionality for group manipulation """
from zope.app.component.hooks import getSite
from Products.CMFCore.utils import getToolByName


def create(groupname=None,
           title=None,
           description=None,
           roles=[],
           groups=[]):
    """Create a group.

    :param groupname: [required] Name of the new group.
    :type groupname: string
    :param title: Title of the new group
    :type title: string
    :param description: Description of the new group
    :type description: string
    :param roles: Roles to assign to this group
    :type roles: list
    :param groups: Groups that belong to this group
    :type groups: list
    :returns: Newly created group
    :rtype: GroupData object
    :Example: :ref:`group_create_example`
    """
    if not groupname:
        raise ValueError('You have to pass the groupname parameter!')

    group_tool = getToolByName(getSite(), 'portal_groups')

    group_tool.addGroup(
        groupname, roles, groups, title=title,
        description=description)
    return group_tool.getGroupById(groupname)


def get(groupname=None):
    """Get a group.

    :param groupname: [required] Name of the group we want to get.
    :type groupname: string
    :returns: Group
    :rtype: GroupData object
    :Example: :ref:`group_get_example`
    """
    if not groupname:
        raise ValueError('You have to pass the groupname parameter!')

    group_tool = getToolByName(getSite(), 'portal_groups')
    return group_tool.getGroupById(groupname)


def get_all():
    """Get all groups.

    :returns: All groups
    :rtype: List of GroupData objects
    :Example: :ref:`groups_get_all_example`
    """
    group_tool = getToolByName(getSite(), 'portal_groups')
    return group_tool.listGroups()


def delete(groupname=None, group=None):
    """Delete a group.

    Arguments ``groupname`` and ``group`` are mutually exclusive. You can
    either set one or the other, but not both.

    :param groupname: Name of the group to be deleted.
    :type groupname: string
    :param group: Group object to be deleted.
    :type group: GroupData object
    :Example: :ref:`group_delete_example`
    """
    if not groupname and not group:
        raise ValueError

    if groupname and group:
        raise ValueError

    group_tool = getToolByName(getSite(), 'portal_groups')

    if group:
        groupname = group.id

    return group_tool.removeGroup(groupname)


def add_user(groupname=None, group=None, username=None, user=None):
    """Add the user to a group.

    Arguments ``groupname`` and ``group`` are mutually exclusive. You can
    either set one or the other, but not both.

    Arguments ``username`` and ``user`` are mutually exclusive. You can
    either set one or the other, but not both.

    :param groupname: Name of the group to which to add the user.
    :type groupname: string
    :param group: Group to which to add the user.
    :type group: GroupData object
    :param username: Username of the user to add to the group.
    :type username: string
    :param user: User to add to the group.
    :type user: MemberData object

    :Example: :ref:`add_user_to_group_example`
    """
    if not username and not user:
        raise ValueError

    if username and user:
        raise ValueError

    if not groupname and not group:
        raise ValueError

    if groupname and group:
        raise ValueError

    user_id = username or user.id
    group_id = groupname or group.id
    portal_groups = getToolByName(getSite(), 'portal_groups')
    portal_groups.addPrincipalToGroup(user_id, group_id)


def delete_user(groupname=None, group=None, username=None, user=None):
    """Remove the user from a group.

    Arguments ``groupname`` and ``group`` are mutually exclusive. You can
    either set one or the other, but not both.

    Arguments ``username`` and ``user`` are mutually exclusive. You can either
    set one or the other, but not both.

    :param groupname: Name of the group to remove the user from.
    :type groupname: string
    :param group: Group to remove the user from.
    :type group: GroupData object
    :param username: Username of the user to delete from the group.
    :type username: string
    :param user: User to delete from the group.
    :type user: MemberData object

    :Example: :ref:`delete_user_from_group_example`
    """
    if not username and not user:
        raise ValueError

    if username and user:
        raise ValueError

    if not groupname and not group:
        raise ValueError

    if groupname and group:
        raise ValueError

    user_id = username or user.id
    group_id = groupname or group.id
    portal_groups = getToolByName(getSite(), 'portal_groups')
    portal_groups.removePrincipalFromGroup(user_id, group_id)
