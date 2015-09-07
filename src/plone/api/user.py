# -*- coding: utf-8 -*-
"""Module that provides functionality for user manipulation."""

from AccessControl.Permission import getPermissions
from Products.CMFPlone.RegistrationTool import get_member_by_login_name
from contextlib import contextmanager
from plone.api import env
from plone.api import portal
from plone.api.exc import GroupNotFoundError
from plone.api.exc import InvalidParameterError
from plone.api.exc import MissingParameterError
from plone.api.exc import UserNotFoundError
from plone.api.validation import at_least_one_of
from plone.api.validation import mutually_exclusive_parameters
from plone.api.validation import required_parameters

import random
import string


def create(
    email=None,
    username=None,
    password=None,
    roles=('Member', ),
    properties=None
):
    """Create a user.

    :param email: [required] Email for the new user.
    :type email: string
    :param username: Username for the new user. This is required if email
        is not used as a username.
    :type username: string
    :param password: Password for the new user. If it's not set we generate
        a random 8-char alpha-numeric one.
    :type password: string
    :param properties: User properties to assign to the new user. The list of
        available properties is available in ``portal_memberdata`` through ZMI.
    :type properties: dict
    :returns: Newly created user
    :rtype: MemberData object
    :raises:
        MissingParameterError
        InvalidParameterError
    :Example: :ref:`user_create_example`
    """
    if properties is None:
        # Never use a dict as default for a keyword argument.
        properties = {}

    # it may happen that someone passes email in the properties dict, catch
    # that and set the email so the code below this works fine
    if not email and properties.get('email'):
        email = properties.get('email')

    if not email:
        raise MissingParameterError("You need to pass the new user's email.")

    try:
        use_email_as_username = portal.get_registry_record(
            'plone.use_email_as_login')
    except InvalidParameterError:
        site = portal.get()
        props = site.portal_properties
        use_email_as_username = props.site_properties.use_email_as_login

    if not use_email_as_username and not username:
        raise InvalidParameterError(
            "The portal is configured to use username "
            "that is not email so you need to pass a username."
        )

    registration = portal.get_tool('portal_registration')
    user_id = use_email_as_username and email or username

    # Generate a random 8-char password
    if not password:
        chars = string.ascii_letters + string.digits
        password = ''.join(random.choice(chars) for x in range(8))

    properties.update(username=user_id)
    properties.update(email=email)

    registration.addMember(
        user_id,
        password,
        roles,
        properties=properties
    )
    return get(username=user_id)


@mutually_exclusive_parameters('userid', 'username')
@at_least_one_of('userid', 'username')
def get(userid=None, username=None):
    """Get a user.

    Plone provides both a unique, unchanging identifier for a user (the
    userid) and a username, which is the value a user types into the login
    form. In many cases, the values for each will be the same, but under some
    circumstances they will differ. Known instances of this behavior include:

     * using content-based members via membrane
     * users changing their email address when using email as login is enabled

    We provide the ability to look up users by either.

    :param userid: Userid of the user we want to get.
    :type userid: string
    :param username: Username of the user we want to get.
    :type username: string
    :returns: User
    :rtype: MemberData object
    :raises:
        MissingParameterError
    :Example: :ref:`user_get_example`
    """
    if userid is not None:
        portal_membership = portal.get_tool('portal_membership')
        return portal_membership.getMemberById(userid)

    return get_member_by_login_name(
        portal.get(),
        username,
        raise_exceptions=False
    )


def get_current():
    """Get the currently logged-in user.

    :returns: Currently logged-in user
    :rtype: MemberData object
    :Example: :ref:`user_get_current_example`
    """
    portal_membership = portal.get_tool('portal_membership')
    return portal_membership.getAuthenticatedMember()


@mutually_exclusive_parameters('groupname', 'group')
def get_users(groupname=None, group=None):
    """Get all users or all users filtered by group.

    Arguments ``group`` and ``groupname`` are mutually exclusive.
    You can either set one or the other, but not both.

    :param groupname: Groupname of the group of which to return users. If set,
        only return users that are member of this group.
    :type username: string
    :param group: Group of which to return users.
        If set, only return users that are member of this group.
    :type group: GroupData object
    :returns: All users (optionlly filtered by group)
    :rtype: List of MemberData objects
    :Example: :ref:`user_get_all_users_example`,
        :ref:`user_get_groups_users_example`
    """
    if groupname:
        group_tool = portal.get_tool('portal_groups')
        group = group_tool.getGroupById(groupname)
        if not group:
            raise GroupNotFoundError

    portal_membership = portal.get_tool('portal_membership')

    if group:
        return group.getGroupMembers()
    else:
        return portal_membership.listMembers()


@mutually_exclusive_parameters('username', 'user')
@at_least_one_of('username', 'user')
def delete(username=None, user=None):
    """Delete a user.

    Arguments ``username`` and ``user`` are mutually exclusive. You can either
    set one or the other, but not both.

    :param username: Username of the user to be deleted.
    :type username: string
    :param user: User object to be deleted.
    :type user: MemberData object
    :raises:
        MissingParameterError
        InvalidParameterError
    :Example: :ref:`user_delete_example`
    """
    portal_membership = portal.get_tool('portal_membership')
    user_id = username or user.id
    portal_membership.deleteMembers((user_id,))


def is_anonymous():
    """Check if the currently logged-in user is anonymous.

    :returns: True if the current user is anonymous, False otherwise.
    :rtype: bool
    :Example: :ref:`user_is_anonymous_example`
    """
    return bool(portal.get_tool('portal_membership').isAnonymousUser())


@mutually_exclusive_parameters('username', 'user')
def get_roles(username=None, user=None, obj=None, inherit=True):
    """Get user's site-wide or local roles.

    Arguments ``username`` and ``user`` are mutually exclusive. You
    can either set one or the other, but not both. if ``username`` and
    ``user`` are not given, the currently authenticated member will be used.

    :param username: Username of the user for which to get roles.
    :type username: string
    :param user: User object for which to get roles.
    :type user: MemberData object
    :param obj: If obj is set then return local roles on this context.
        If obj is not given, the site root local roles will be returned.
    :type obj: content object
    :param inherit: if obj is set and inherit is False, only return
        local roles
    :type inherit: bool
    :raises:
        MissingParameterError
    :Example: :ref:`user_get_roles_example`
    """
    portal_membership = portal.get_tool('portal_membership')

    if username is None:
        if user is None:
            username = portal_membership.getAuthenticatedMember().getId()
        else:
            username = user.getId()

    user = portal_membership.getMemberById(username)
    if user is None:
        raise UserNotFoundError

    if obj is not None:
        if inherit:
            return user.getRolesInContext(obj)
        else:
            return obj.get_local_roles_for_userid(username)
    else:
        return user.getRoles()


@contextmanager
def _nop_context_manager():
    """A trivial context manager that does nothing."""
    yield


@mutually_exclusive_parameters('username', 'user')
def get_permissions(username=None, user=None, obj=None):
    """Get user's site-wide or local permissions.

    Arguments ``username`` and ``user`` are mutually exclusive. You
    can either set one or the other, but not both. if ``username`` and
    ``user`` are not given, the authenticated member will be used.

    :param username: Username of the user for which you want to check
        the permissions.
    :type username: string
    :param user: User object for which you want to check the permissions.
    :type user: MemberData object
    :param obj: If obj is set then check the permissions on this context.
        If obj is not given, the site root will be used.
    :type obj: content object
    :raises:
        InvalidParameterError
    :Example: :ref:`user_get_permissions_example`
    """
    if obj is None:
        obj = portal.get()

    if username is None and user is None:
        context = _nop_context_manager()
    else:
        context = env.adopt_user(username, user)

    result = {}
    with context:
        portal_membership = portal.get_tool('portal_membership')
        permissions = (p[0] for p in getPermissions())
        for permission in permissions:
            result[permission] = bool(
                portal_membership.checkPermission(permission, obj)
            )

    return result


@mutually_exclusive_parameters('username', 'user')
def has_permission(permission, username=None, user=None, obj=None):
    """Check whether this user has the given permssion.

    Arguments ``username`` and ``user`` are mutually exclusive. You
    can either set one or the other, but not both. if ``username`` and
    ``user`` are not given, the authenticated member will be used.

    :param permission: The permission you wish to check
    :type permission: string
    :param username: Username of the user for which you want to check
        the permission.
    :type username: string
    :param user: User object for which you want to check the permission.
    :type user: MemberData object
    :param obj: If obj is set then check the permission on this context.
        If obj is not given, the site root will be used.
    :type obj: content object
    :raises:
        InvalidParameterError
    :returns: True if the user has the permission, False otherwise.
    :rtype: bool
    """
    if obj is None:
        obj = portal.get()

    if username is None and user is None:
        context = _nop_context_manager()
    else:
        context = env.adopt_user(username, user)

    with context:
        portal_membership = portal.get_tool('portal_membership')
        return bool(portal_membership.checkPermission(permission, obj))


@required_parameters('roles')
@mutually_exclusive_parameters('username', 'user')
def grant_roles(username=None, user=None, obj=None, roles=None):
    """Grant roles to a user.

    Arguments ``username`` and ``user`` are mutually exclusive. You
    can either set one or the other, but not both. if ``username`` and
    ``user`` are not given, the authenticated member will be used.

    :param username: Username of the user that will receive the granted roles.
    :type username: string
    :param user: User object that will receive the granted roles.
    :type user: MemberData object
    :param obj: If obj is set then grant roles on this context. If obj is not
        given, the site root will be used.
    :type obj: content object
    :param roles: List of roles to grant
    :type roles: list of strings
    :raises:
        InvalidParameterError
        MissingParameterError
    :Example: :ref:`user_grant_roles_example`
    """
    if user is None:
        user = get(username=username)
    # check we got a user
    if user is None:
        raise InvalidParameterError("User could not be found")

    if isinstance(roles, tuple):
        roles = list(roles)

    # These roles cannot be granted
    if 'Anonymous' in roles or 'Authenticated' in roles:
        raise InvalidParameterError

    roles.extend(get_roles(user=user, obj=obj, inherit=False))

    if obj is None:
        user.setSecurityProfile(roles=roles)
    else:
        obj.manage_setLocalRoles(user.getId(), roles)


@required_parameters('roles')
@mutually_exclusive_parameters('username', 'user')
def revoke_roles(username=None, user=None, obj=None, roles=None):
    """Revoke roles from a user.

    Arguments ``username`` and ``user`` are mutually exclusive. You
    can either set one or the other, but not both. if ``username`` and
    ``user`` are not given, the authenticated member will be used.

    :param username: Username of the user that will receive the revoked roles.
    :type username: string
    :param user: User object that will receive the revoked roles.
    :type user: MemberData object
    :param obj: If obj is set then revoke roles on this context. If obj is not
        given, the site root will be used.
    :type obj: content object
    :param roles: List of roles to revoke
    :type roles: list of strings
    :raises:
        InvalidParameterError
    :Example: :ref:`user_revoke_roles_example`
    """
    if user is None:
        user = get(username=username)
    # check we got a user
    if user is None:
        raise InvalidParameterError("User could not be found")

    if isinstance(roles, tuple):
        roles = list(roles)

    if 'Anonymous' in roles or 'Authenticated' in roles:
        raise InvalidParameterError
    inherit = True
    if obj is not None:
        # if obj, get only a list of local roles, without inherited ones
        inherit = False
    actual_roles = get_roles(user=user, obj=obj, inherit=inherit)
    if actual_roles.count('Anonymous'):
        actual_roles.remove('Anonymous')
    if actual_roles.count('Authenticated'):
        actual_roles.remove('Authenticated')

    roles = list(set(actual_roles) - set(roles))

    if obj is None:
        user.setSecurityProfile(roles=roles)
    elif not roles:
        obj.manage_delLocalRoles([user.getId()])
    else:
        obj.manage_setLocalRoles(user.getId(), roles)
