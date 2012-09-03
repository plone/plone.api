""" Module that provides functionality for user manipulation """

from Products.CMFPlone.utils import getToolByName
from plone.api import portal

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
        ValueError
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
        raise ValueError("You need to pass the new user's email.")

    site = portal.get()
    props = site.portal_properties
    use_email_as_username = props.site_properties.use_email_as_login

    if not use_email_as_username and not username:
        raise ValueError("The portal is configured to use username that is \
            not email so you need to pass a username.")

    registration = getToolByName(site, 'portal_registration')
    user_id = use_email_as_username and email or username

    # Generate a random 8-char password
    if not password:
        chars = string.ascii_letters + string.digits
        password = ''.join(random.choice(chars) for x in range(8))

    properties.update(username=user_id)
    properties.update(email=email)

    return registration.addMember(
        user_id,
        password,
        roles,
        properties=properties
    )


def get(username=None):
    """Get a user.

    :param username: [required] Username of the user we want to get.
    :type username: string
    :returns: User
    :rtype: MemberData object
    :raises:
        ValueError
    :Example: :ref:`user_get_example`
    """
    if not username:
        raise ValueError

    portal_membership = getToolByName(portal.get(), 'portal_membership')
    return portal_membership.getMemberById(username)


def get_current():
    """Get the currently logged-in user.

    :returns: Currently logged-in user
    :rtype: MemberData object
    :raises:
        ValueError
    :Example: :ref:`user_get_current_example`
    """
    portal_membership = getToolByName(portal.get(), 'portal_membership')
    return portal_membership.getAuthenticatedMember()


def get_users(groupname=None, group=None):
    """Get all users or all users filtered by group.

    Arguments ``group`` and ``groupname`` are mutually exclusive. You can either
    set one or the other, but not both.

    :param groupname: Groupname of the group of which to return users. If set,
        only return users that are member of this group.
    :type username: string
    :param user: Group of which to return users. If set, only return users that
        are member of this group.
    :type user: MemberData object
    :returns: All users (optionlly filtered by group)
    :rtype: List of MemberData objects
    :Example: :ref:`user_get_all_users_example`,
        :ref:`user_get_groups_users_example`
    """

    if groupname and group:
        raise ValueError

    if groupname:
        group_tool = getToolByName(portal.get(), 'portal_groups')
        group = group_tool.getGroupById(groupname)
        if not group:
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
        ValueError
    :Example: :ref:`user_delete_example`
    """
    if not username and not user:
        raise ValueError

    if username and user:
        raise ValueError

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
    """Not implemented yet. Get user's site-wide or local roles.

    Arguments ``username`` and ``user`` are mutually exclusive. You can either
    set one or the other, but not both.

    :param username: Username of the user to be deleted.
    :type username: string
    :param user: User object to be deleted.
    :type user: MemberData object
    :param obj: If obj is set then return local roles on this context
    :type obj: content object
    :raises:
        ValueError
    :Example: :ref:`user_get_roles_example`
    """
    raise NotImplementedError


def get_permissions(username=None, user=None, obj=None):
    """Not implemented yet. Get user's site-wide or local permissions.

    Arguments ``username`` and ``user`` are mutually exclusive. You can either
    set one or the other, but not both.

    :param username: Username of the user to be deleted.
    :type username: string
    :param user: User object to be deleted.
    :type user: MemberData object
    :param obj: If obj is set then return local permissions on this context
    :type obj: content object
    :raises:
        ValueError
    :Example: :ref:`user_get_permissions_example`
    """
    raise NotImplementedError


def grant_roles(username=None, user=None, roles=None):
    """Not implemented yet. Grant roles to a user.

    Arguments ``username`` and ``user`` are mutually exclusive. You can either
    set one or the other, but not both.

    :param username: Username of the user to be deleted.
    :type username: string
    :param user: User object to be deleted.
    :type user: MemberData object
    :param roles: List of roles to grant
    :type roles: list of strings
    :raises:
        ValueError
    :Example: :ref:`user_grant_roles_example`
    """
    raise NotImplementedError


def revoke_roles(username=None, user=None, roles=None):
    """Not implemented yet. Revoke roles from a user.

    Arguments ``username`` and ``user`` are mutually exclusive. You can either
    set one or the other, but not both.

    :param username: Username of the user to be deleted.
    :type username: string
    :param user: User object to be deleted.
    :type user: MemberData object
    :param roles: List of roles to grant
    :type roles: list of strings
    :raises:
        ValueError
    :Example: :ref:`user_revoke_roles_example`
    """
    raise NotImplementedError
