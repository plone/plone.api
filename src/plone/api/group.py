""" Module that provides functionality for group manipulation """
from Products.CMFCore.utils import getToolByName
from plone.api import portal


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
    :raises:
        ValueError
    :Example: :ref:`group_create_example`
    """
    if not groupname:
        raise ValueError('You have to pass the groupname parameter!')

    group_tool = getToolByName(portal.get(), 'portal_groups')

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
    :raises:
        ValueError
    :Example: :ref:`group_get_example`
    """
    if not groupname:
        raise ValueError('You have to pass the groupname parameter!')

    group_tool = getToolByName(portal.get(), 'portal_groups')
    return group_tool.getGroupById(groupname)


def get_groups(username=None, user=None):
    """Get all groups or all groups filtered by user.

    Arguments ``username`` and ``user`` are mutually exclusive. You can either
    set one or the other, but not both.

    :param username: Username of the user for which to return groups. If set,
        only return groups that this user is member of.
    :type username: string
    :param user: User for which to return groups. If set, only return groups
        that this user is member of.
    :type user: MemberData object
    :returns: All groups (optionlly filtered by user)
    :rtype: List of GroupData objects
    :Example: :ref:`group_get_all_groups_example`,
        :ref:`group_get_users_groups_example`
    """
    if username and user:
        raise ValueError

    if username:
        membership = getToolByName(portal.get(), 'portal_membership')
        user = membership.getMemberById(username)
        if not user:
            raise ValueError

    group_tool = getToolByName(portal.get(), 'portal_groups')

    if user:
        groups = group_tool.getGroupsForPrincipal(user)
        return [get(groupname=group) for group in groups]
    else:
        return group_tool.listGroups()


def delete(groupname=None, group=None):
    """Delete a group.

    Arguments ``groupname`` and ``group`` are mutually exclusive. You can
    either set one or the other, but not both.

    :param groupname: Name of the group to be deleted.
    :type groupname: string
    :param group: Group object to be deleted.
    :type group: GroupData object
    :raises:
        ValueError
    :Example: :ref:`group_delete_example`
    """
    if not groupname and not group:
        raise ValueError

    if groupname and group:
        raise ValueError

    group_tool = getToolByName(portal.get(), 'portal_groups')

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
    :raises:
        ValueError
    :Example: :ref:`group_add_user_example`
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
    portal_groups = getToolByName(portal.get(), 'portal_groups')
    portal_groups.addPrincipalToGroup(user_id, group_id)


def remove_user(groupname=None, group=None, username=None, user=None):
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
    :raises:
        ValueError
    :Example: :ref:`group_remove_user_example`
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
    portal_groups = getToolByName(portal.get(), 'portal_groups')
    portal_groups.removePrincipalFromGroup(user_id, group_id)


def get_roles(groupname=None, group=None, obj=None):
    """Not implemented yet. Get group's site-wide or local roles.

    Arguments ``groupname`` and ``group`` are mutually exclusive. You can
    either set one or the other, but not both.

    :param groupname: Name of the group to remove the user from.
    :type groupname: string
    :param group: Group to remove the user from.
    :type group: GroupData object
    :param obj: If obj is set then return local roles on this context
    :type obj: content object
    :raises:
        ValueError
    :Example: :ref:`group_get_roles_example`
    """
    raise NotImplementedError


def get_permissions(groupname=None, group=None, obj=None):
    """Not implemented yet. Get group's site-wide or local permissions.

    Arguments ``groupname`` and ``group`` are mutually exclusive. You can
    either set one or the other, but not both.

    :param groupname: Name of the group to remove the user from.
    :type groupname: string
    :param group: Group to remove the user from.
    :type group: GroupData object
    :param obj: If obj is set then return local permissions on this context
    :type obj: content object
    :raises:
        ValueError
    :Example: :ref:`group_get_permissions_example`
    """
    raise NotImplementedError


def grant_roles(groupname=None, group=None, roles=None):
    """Not implemented yet. Grant roles to a group.

    Arguments ``groupname`` and ``group`` are mutually exclusive. You can
    either set one or the other, but not both.

    :param groupname: Name of the group to remove the user from.
    :type groupname: string
    :param group: Group to remove the user from.
    :type group: GroupData object
    :param roles: List of roles to grant
    :type roles: list of strings
    :raises:
        ValueError
    :Example: :ref:`group_grant_roles_example`
    """
    raise NotImplementedError


def revoke_roles(groupname=None, group=None, roles=None):
    """Not implemented yet. Revoke roles from a group.

    Arguments ``groupname`` and ``group`` are mutually exclusive. You can
    either set one or the other, but not both.

    :param groupname: Name of the group to remove the user from.
    :type groupname: string
    :param group: Group to remove the user from.
    :type group: GroupData object
    :param roles: List of roles to grant
    :type roles: list of strings
    :raises:
        ValueError
    :Example: :ref:`group_revoke_roles_example`
    """
    raise NotImplementedError
