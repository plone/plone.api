# -*- coding: utf-8 -*-
"""Module that provides functionality for group manipulation."""

from plone.api import portal
from plone.api.exc import GroupNotFoundError
from plone.api.exc import UserNotFoundError
from plone.api.user import get as user_get
from plone.api.validation import at_least_one_of
from plone.api.validation import mutually_exclusive_parameters
from plone.api.validation import required_parameters


@required_parameters('groupid')
def create(
    groupid=None,
    title=None,
    description=None,
    roles=[],
    groups=[]
):
    """Create a group.

    :param groupid: [required] Name of the new group.
    :type groupid: string
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
    group_tool = portal.get_tool('portal_groups')
    group_tool.addGroup(
        groupid, roles, groups,
        title=title,
        description=description
    )
    return group_tool.getGroupById(groupid)


@required_parameters('groupid')
def get(groupid=None):
    """Get a group.

    :param groupid: [required] Name of the group we want to get.
    :type groupid: string
    :returns: Group
    :rtype: GroupData object
    :raises:
        ValueError
    :Example: :ref:`group_get_example`
    """
    group_tool = portal.get_tool('portal_groups')
    return group_tool.getGroupById(groupid)


@mutually_exclusive_parameters('username', 'user')
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
    :raises: UserNotFoundError
    :Example: :ref:`group_get_all_groups_example`,
        :ref:`group_get_users_groups_example`
    """
    if username:
        user = user_get(username=username)
        if not user:
            raise UserNotFoundError

    group_tool = portal.get_tool('portal_groups')

    if user:
        groups = group_tool.getGroupsForPrincipal(user)
        return [get(groupid=group) for group in groups]

    return group_tool.listGroups()


@mutually_exclusive_parameters('groupid', 'group')
@at_least_one_of('groupid', 'group')
def delete(groupid=None, group=None):
    """Delete a group.

    Arguments ``groupid`` and ``group`` are mutually exclusive. You can
    either set one or the other, but not both.

    :param groupid: Name of the group to be deleted.
    :type groupid: string
    :param group: Group object to be deleted.
    :type group: GroupData object
    :raises:
        ValueError
    :Example: :ref:`group_delete_example`
    """
    group_tool = portal.get_tool('portal_groups')

    if group:
        groupid = group.id

    return group_tool.removeGroup(groupid)


@mutually_exclusive_parameters('groupid', 'group')
@at_least_one_of('groupid', 'group')
@mutually_exclusive_parameters('username', 'user')
@at_least_one_of('username', 'user')
def add_user(groupid=None, group=None, username=None, user=None):
    """Add the user to a group.

    Arguments ``groupid`` and ``group`` are mutually exclusive. You can
    either set one or the other, but not both.

    Arguments ``username`` and ``user`` are mutually exclusive. You can
    either set one or the other, but not both.

    :param groupid: Name of the group to which to add the user.
    :type groupid: string
    :param group: Group to which to add the user.
    :type group: GroupData object
    :param username: Username of the user to add to the group.
    :type username: string
    :param user: User to add to the group.
    :type user: MemberData object
    :raises:
        ValueError
        UserNotFoundError
    :Example: :ref:`group_add_user_example`

    """
    if username:
        user = user_get(username=username)
        if not user:
            raise UserNotFoundError

    user_id = user.id
    groupid = groupid or group.id
    portal_groups = portal.get_tool('portal_groups')
    portal_groups.addPrincipalToGroup(user_id, groupid)


@mutually_exclusive_parameters('groupid', 'group')
@at_least_one_of('groupid', 'group')
@mutually_exclusive_parameters('username', 'user')
@at_least_one_of('username', 'user')
def remove_user(groupid=None, group=None, username=None, user=None):
    """Remove the user from a group.

    Arguments ``groupid`` and ``group`` are mutually exclusive. You can
    either set one or the other, but not both.

    Arguments ``username`` and ``user`` are mutually exclusive. You can either
    set one or the other, but not both.

    :param groupid: Name of the group to remove the user from.
    :type groupid: string
    :param group: Group to remove the user from.
    :type group: GroupData object
    :param username: Username of the user to delete from the group.
    :type username: string
    :param user: User to delete from the group.
    :type user: MemberData object
    :raises:
        ValueError
        UserNotFoundError
    :Example: :ref:`group_remove_user_example`
    """
    if username:
        user = user_get(username=username)
        if not user:
            raise UserNotFoundError
    user_id = user.id
    groupid = groupid or group.id
    portal_groups = portal.get_tool('portal_groups')
    portal_groups.removePrincipalFromGroup(user_id, groupid)


@mutually_exclusive_parameters('groupid', 'group')
@at_least_one_of('groupid', 'group')
def get_roles(groupid=None, group=None, obj=None):
    """Get group's site-wide or local roles.

    Arguments ``groupid`` and ``group`` are mutually exclusive. You can
    either set one or the other, but not both.

    :param groupid: Name of the group to get roles from.
    :type groupid: string
    :param group: Group to get roles from.
    :type group: GroupData object
    :param obj: If obj is set then return local roles on this context.
    :type obj: content object
    :raises:
        ValueError
    :Example: :ref:`group_get_roles_example`
    """
    groupid = groupid or group.id

    group = get(groupid=groupid)
    if group is None:
        raise GroupNotFoundError

    group = group.getGroup()
    # when context obj is available we bypass getRolesInContext method
    # from PloneGroup class to use PloneUser class implementation because
    # PloneGroup class disables all local roles support
    # see: Products.PlonePAS.plugins.group.PloneGroup
    return group.getRoles() if obj is None else \
        super(group.__class__, group).getRolesInContext(obj)


@required_parameters('roles')
@mutually_exclusive_parameters('groupid', 'group')
@at_least_one_of('groupid', 'group')
def grant_roles(groupid=None, group=None, roles=None, obj=None):
    """Grant roles to a group.

    Arguments ``groupid`` and ``group`` are mutually exclusive. You can
    either set one or the other, but not both.

    :param groupid: Name of the group to grant roles to.
    :type groupid: string
    :param group: Group to grant roles to.
    :type group: GroupData object
    :param roles: List of roles to grant
    :type roles: list of strings
    :param obj: If obj is set then grant local roles on this context.
    :type obj: content object
    :raises:
        ValueError
    :Example: :ref:`group_grant_roles_example`
    """
    if 'Anonymous' in roles or 'Authenticated' in roles:
        raise ValueError

    groupid = groupid or group.id

    actual_roles = get_roles(groupid=groupid, obj=obj)
    if actual_roles.count('Anonymous'):
        actual_roles.remove('Anonymous')
    if actual_roles.count('Authenticated'):
        actual_roles.remove('Authenticated')

    roles = list(set(actual_roles) | set(roles))
    portal_groups = portal.get_tool('portal_groups')

    if obj is None:
        portal_groups.setRolesForGroup(group_id=groupid, roles=roles)
    else:
        obj.manage_setLocalRoles(groupid, roles)


@required_parameters('roles')
@mutually_exclusive_parameters('groupid', 'group')
@at_least_one_of('groupid', 'group')
def revoke_roles(groupid=None, group=None, roles=None, obj=None):
    """Revoke roles from a group.

    Arguments ``groupid`` and ``group`` are mutually exclusive. You can
    either set one or the other, but not both.

    :param groupid: Name of the group to revoke roles to.
    :type groupid: string
    :param group: Group to revoke roles to.
    :type group: GroupData object
    :param roles: List of roles to revoke
    :type roles: list of strings
    :param obj: If obj is set then revoke local roles on this context.
    :type obj: content object
    :raises:
        ValueError
    :Example: :ref:`group_revoke_roles_example`
    """
    if 'Anonymous' in roles or 'Authenticated' in roles:
        raise ValueError

    groupid = groupid or group.id

    actual_roles = get_roles(groupid=groupid, obj=obj)
    if actual_roles.count('Anonymous'):
        actual_roles.remove('Anonymous')
    if actual_roles.count('Authenticated'):
        actual_roles.remove('Authenticated')

    roles = list(set(actual_roles) - set(roles))
    portal_groups = portal.get_tool('portal_groups')

    if obj is None:
        portal_groups.setRolesForGroup(group_id=groupid, roles=roles)
    elif roles:
        obj.manage_setLocalRoles(groupid, roles)
    else:
        obj.manage_delLocalRoles([groupid])
