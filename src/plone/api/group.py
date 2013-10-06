# -*- coding: utf-8 -*-
"""Module that provides functionality for group manipulation."""

from plone.api import portal
from plone.api.exc import GroupNotFoundError
from plone.api.exc import UserNotFoundError
from plone.api.user import get as user_get
from plone.api.validation import at_least_one_of
from plone.api.validation import mutually_exclusive_parameters
from plone.api.validation import required_parameters


@required_parameters('groupname')
def create(
    groupname=None,
    title=None,
    description=None,
    roles=[],
    groups=[]
):
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
    group_tool = portal.get_tool('portal_groups')
    group_tool.addGroup(
        groupname, roles, groups,
        title=title,
        description=description
    )
    return group_tool.getGroupById(groupname)


@required_parameters('groupname')
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
    group_tool = portal.get_tool('portal_groups')
    return group_tool.getGroupById(groupname)


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
        return [get(groupname=group) for group in groups]

    return group_tool.listGroups()


@mutually_exclusive_parameters('groupname', 'group')
@at_least_one_of('groupname', 'group')
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
    group_tool = portal.get_tool('portal_groups')

    if group:
        groupname = group.id

    return group_tool.removeGroup(groupname)


@mutually_exclusive_parameters('groupname', 'group')
@at_least_one_of('groupname', 'group')
@mutually_exclusive_parameters('username', 'user')
@at_least_one_of('username', 'user')
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
        UserNotFoundError
    :Example: :ref:`group_add_user_example`

    """
    if username:
        user = user_get(username=username)
        if not user:
            raise UserNotFoundError

    user_id = user.id
    group_id = groupname or group.id
    portal_groups = portal.get_tool('portal_groups')
    portal_groups.addPrincipalToGroup(user_id, group_id)


@mutually_exclusive_parameters('groupname', 'group')
@at_least_one_of('groupname', 'group')
@mutually_exclusive_parameters('username', 'user')
@at_least_one_of('username', 'user')
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
        UserNotFoundError
    :Example: :ref:`group_remove_user_example`
    """
    if username:
        user = user_get(username=username)
        if not user:
            raise UserNotFoundError
    user_id = user.id
    group_id = groupname or group.id
    portal_groups = portal.get_tool('portal_groups')
    portal_groups.removePrincipalFromGroup(user_id, group_id)


@mutually_exclusive_parameters('groupname', 'group')
@at_least_one_of('groupname', 'group')
def get_roles(groupname=None, group=None, obj=None):
    """Get group's site-wide or local roles.

    Arguments ``groupname`` and ``group`` are mutually exclusive. You can
    either set one or the other, but not both.

    :param groupname: Name of the group to get roles from.
    :type groupname: string
    :param group: Group to get roles from.
    :type group: GroupData object
    :param obj: If obj is set then return local roles on this context.
    :type obj: content object
    :raises:
        ValueError
    :Example: :ref:`group_get_roles_example`
    """
    group_id = groupname or group.id

    group = get(groupname=group_id)
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
@mutually_exclusive_parameters('groupname', 'group')
@at_least_one_of('groupname', 'group')
def grant_roles(groupname=None, group=None, roles=None, obj=None):
    """Grant roles to a group.

    Arguments ``groupname`` and ``group`` are mutually exclusive. You can
    either set one or the other, but not both.

    :param groupname: Name of the group to grant roles to.
    :type groupname: string
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

    group_id = groupname or group.id

    actual_roles = get_roles(groupname=group_id, obj=obj)
    if actual_roles.count('Anonymous'):
        actual_roles.remove('Anonymous')
    if actual_roles.count('Authenticated'):
        actual_roles.remove('Authenticated')

    roles = list(set(actual_roles) | set(roles))
    portal_groups = portal.get_tool('portal_groups')

    if obj is None:
        portal_groups.setRolesForGroup(group_id=group_id, roles=roles)
    else:
        obj.manage_setLocalRoles(group_id, roles)


@required_parameters('roles')
@mutually_exclusive_parameters('groupname', 'group')
@at_least_one_of('groupname', 'group')
def revoke_roles(groupname=None, group=None, roles=None, obj=None):
    """Revoke roles from a group.

    Arguments ``groupname`` and ``group`` are mutually exclusive. You can
    either set one or the other, but not both.

    :param groupname: Name of the group to revoke roles to.
    :type groupname: string
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

    group_id = groupname or group.id

    actual_roles = get_roles(groupname=group_id, obj=obj)
    if actual_roles.count('Anonymous'):
        actual_roles.remove('Anonymous')
    if actual_roles.count('Authenticated'):
        actual_roles.remove('Authenticated')

    roles = list(set(actual_roles) - set(roles))
    portal_groups = portal.get_tool('portal_groups')

    if obj is None:
        portal_groups.setRolesForGroup(group_id=group_id, roles=roles)
    elif roles:
        obj.manage_setLocalRoles(group_id, roles)
    else:
        obj.manage_delLocalRoles([group_id])
