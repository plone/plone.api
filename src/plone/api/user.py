# -*- coding: utf-8 -*-
"""Module that provides functionality for user manipulation."""

from AccessControl.Permission import getPermissions
from AccessControl.SecurityManagement import getSecurityManager
from AccessControl.SecurityManagement import newSecurityManager
from AccessControl.SecurityManagement import setSecurityManager
from plone.api import portal
from plone.api.exc import InvalidParameterError
from plone.api.exc import MissingParameterError
from Products.CMFPlone.utils import getToolByName
from zope.globalrequest import getRequest

import random
import string


def create(email=None, username=None, password=None, roles=('Member', ),
           properties=None):
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

    site = portal.get()
    props = site.portal_properties
    use_email_as_username = props.site_properties.use_email_as_login

    if not use_email_as_username and not username:
        raise InvalidParameterError("The portal is configured to use username \
        that is not email so you need to pass a username.")

    registration = getToolByName(site, 'portal_registration')
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


def get(username=None):
    """Get a user.

    :param username: [required] Username of the user we want to get.
    :type username: string
    :returns: User
    :rtype: MemberData object
    :raises:
        MissingParameterError
    :Example: :ref:`user_get_example`

    """
    if not username:
        raise MissingParameterError

    portal_membership = getToolByName(portal.get(), 'portal_membership')
    return portal_membership.getMemberById(username)


def get_current():
    """Get the currently logged-in user.

    :returns: Currently logged-in user
    :rtype: MemberData object
    :Example: :ref:`user_get_current_example`

    """
    portal_membership = getToolByName(portal.get(), 'portal_membership')
    return portal_membership.getAuthenticatedMember()


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

    if groupname and group:
        raise InvalidParameterError

    if groupname:
        group_tool = getToolByName(portal.get(), 'portal_groups')
        group = group_tool.getGroupById(groupname)
        if not group:
            # XXX This should raise a custom plone.api exception
            raise ValueError

    portal_membership = getToolByName(portal.get(), 'portal_membership')

    if group:
        return group.getGroupMembers()
    else:
        return portal_membership.listMembers()


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
    if not username and not user:
        raise MissingParameterError

    if username and user:
        raise InvalidParameterError

    portal_membership = getToolByName(portal.get(), 'portal_membership')
    user_id = username or user.id
    portal_membership.deleteMembers((user_id,))


def is_anonymous():
    """Check if the currently logged-in user is anonymous.

    :returns: True if the current user is anonymous, False otherwise.
    :rtype: bool
    :Example: :ref:`user_is_anonymous_example`

    """
    return getToolByName(portal.get(), 'portal_membership').isAnonymousUser()


def get_roles(username=None, user=None, obj=None):
    """Get user's site-wide or local roles.

    Arguments ``username`` and ``user`` are mutually exclusive. You
    can either set one or the other, but not both. if ``username`` and
    ``user`` are not given, the authenticated member will be used.

    :param username: Username of the user for which to get roles.
    :type username: string
    :param user: User object for which to get roles.
    :type user: MemberData object
    :param obj: If obj is set then return local roles on this context.
        If obj is not given, the site root local roles will be returned.
    :type obj: content object
    :raises:
        MissingParameterError
    :Example: :ref:`user_get_roles_example`

    """

    if username and user:
        raise InvalidParameterError

    portal_membership = getToolByName(portal.get(), 'portal_membership')

    if username is None:
        if user is None:
            username = portal_membership.getAuthenticatedMember().getId()
        else:
            username = user.getId()

    user = portal_membership.getMemberById(username)
    if user is None:
        # XXX This needs a custom plone.api error
        raise ValueError

    return user.getRolesInContext(obj) if obj is not None else user.getRoles()


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

    if username and user:
        raise InvalidParameterError

    if obj is None:
        obj = portal.get()

    # holds the initial security context
    current_security_manager = getSecurityManager()

    portal_membership = getToolByName(portal.get(), 'portal_membership')

    if username is None:
        if user is None:
            username = portal_membership.getAuthenticatedMember().getId()
        else:
            username = user.getId()

    user = portal_membership.getMemberById(username)
    if user is None:
        # XXX This needs a custom plone.api error
        raise ValueError
    newSecurityManager(getRequest(), user)

    permissions = (p[0] for p in getPermissions())
    d = {}
    for permission in permissions:
        d[permission] = bool(user.checkPermission(permission, obj))

    # restore the initial security context
    setSecurityManager(current_security_manager)

    return d


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

    if username and user:
        raise InvalidParameterError

    if roles is None:
        raise MissingParameterError

    if user is None:
        user = get(username=username)

    if isinstance(roles, tuple):
        roles = list(roles)

    # These roles cannot be granted
    if 'Anonymous' in roles or 'Authenticated' in roles:
        raise InvalidParameterError

    roles.extend(get_roles(user=user, obj=obj))

    if obj is None:
        user.setSecurityProfile(roles=roles)
    else:
        obj.manage_setLocalRoles(user.getId(), roles)


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
    if username and user:
        raise InvalidParameterError

    if roles is None:
        raise MissingParameterError

    if user is None:
        user = get(username=username)

    if isinstance(roles, tuple):
        roles = list(roles)

    if 'Anonymous' in roles or 'Authenticated' in roles:
        raise InvalidParameterError

    actual_roles = get_roles(user=user, obj=obj)
    if actual_roles.count('Anonymous'):
        actual_roles.remove('Anonymous')
    if actual_roles.count('Authenticated'):
        actual_roles.remove('Authenticated')

    roles = list(set(actual_roles) - set(roles))

    if obj is None:
        user.setSecurityProfile(roles=roles)
    else:
        obj.manage_setLocalRoles(user.getId(), roles)
