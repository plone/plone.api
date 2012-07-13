""" Module that provides functionality for user manipulation """
from AccessControl.ImplPython import rolesForPermissionOn
from Products.CMFPlone.utils import getToolByName
from zope.app.component.hooks import getSite

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

    site = getSite()
    props = site.portal_properties
    use_email_as_username = props.site_properties.use_email_as_login

    if not use_email_as_username and not username:
        raise ValueError("The portal is configured to use username that is "
            "not email so you need to pass a username.")

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
    :Example: :ref:`user_get_example`
    """
    if not username:
        raise ValueError

    portal_membership = getToolByName(getSite(), 'portal_membership')
    return portal_membership.getMemberById(username)


def get_current():
    """Get the currently logged-in user.

    :returns: Currently logged-in user
    :rtype: MemberData object
    :Example: :ref:`user_get_current_example`
    """
    portal_membership = getToolByName(getSite(), 'portal_membership')
    return portal_membership.getAuthenticatedMember()


def get_all():
    """Return all users.

    :returns: All users
    :rtype: List of MemberData objects
    :Example: :ref:`users_get_all_example`
    """
    portal_membership = getToolByName(getSite(), 'portal_membership')
    return portal_membership.listMembers()


def delete(username=None, user=None):
    """Delete a user.

    Arguments ``username`` and ``user`` are mutually exclusive. You can either
    set one or the other, but not both.

    :param username: Username of the user to be deleted.
    :type username: string
    :param user: User object to be deleted.
    :type user: MemberData object
    :Example: :ref:`user_delete_example`
    """
    if not username and not user:
        raise ValueError

    if username and user:
        raise ValueError

    portal_membership = getToolByName(getSite(), 'portal_membership')
    user_id = username or user.id
    portal_membership.deleteMembers((user_id,))


def get_groups(username=None, user=None):
    """Get a list of groups that this user is a member of.

    Arguments ``username`` and ``user`` are mutually exclusive. You can either
    set one or the other, but not both.

    :param username: Username of the user for which to return groups.
    :type username: string
    :param user: User for which to return groups.
    :type user: MemberData object
    :returns: List of names of groups this user is a member of.
    :rtype: List of strings
    :Example: :ref:`get_groups_for_user_example`
    """
    if not username and not user:
        raise ValueError

    if username and user:
        raise ValueError

    site = getSite()

    if username:
        user = getToolByName(site, 'portal_membership').getMemberById(username)
    return getToolByName(site, 'portal_groups').getGroupsForPrincipal(user)


def is_anonymous():
    """Check if the currently logged-in user is anonymous.

    :returns: True if the current user is anonymous, False otherwise.
    :rtype: bool
    :Example: :ref:`user_is_anonymous_example`
    """
    return getToolByName(getSite(), 'portal_membership').isAnonymousUser()


def has_role(role=None, username=None, user=None):
    """Check if the user has the specified role.

    Arguments ``username`` and ``user`` are mutually exclusive. You can either
    set one or the other, but not both. If no ``username` or ``user`` are
    provided, check the role for the currently logged-in user.

    :param role: [required] Role of the user to check for
    :type role: string
    :param username: Username of the user that we are checking the role for
    :type username: string
    :param user: User that we are checking the role for
    :type user: MemberData object
    :returns: True if user has the specified role, False otherwise.
    :rtype: bool
    :Example: :ref:`user_has_role_example`
    """
    if not role:
        raise ValueError

    if username and user:
        raise ValueError

    portal_membership = getToolByName(getSite(), 'portal_membership')
    current_user = portal_membership.getAuthenticatedMember()

    if username:
        user = portal_membership.getMemberById(username)

    if not user or user == current_user:
        return role in current_user.getRoles()
    else:
        return role in user.getRoles()


def has_permission(permission=None, username=None, user=None,
                   object=None):
    """Check if the user has the specified permission on the given object.

    Arguments ``username`` and ``user`` are mutually exclusive. You can either
    set one or the other, but not both. If no ``username` or ``user`` are
    provided, check the permission for the currently logged-in user.

    :param permission: [required] Permission of the user to check for
    :type permission: string
    :param username: Username of the user that we are checking the permission
        for
    :type username: string
    :param user: User that we are checking the permission for
    :type user: MemberData object
    :param object: Object that we are checking the permission for
    :type object: object
    :returns: True if user has the specified permission, False otherwise.
    :rtype: bool
    :Example: :ref:`user_has_permission_example`
    """
    if not permission:
        ValueError

    if username and user:
        raise ValueError

    if not object:
        raise ValueError

    portal_membership = getToolByName(getSite(), 'portal_membership')
    if username:
        user = portal_membership.getMemberById(username)

    if not user or user == portal_membership.getAuthenticatedMember():
        return portal_membership.checkPermission(permission, object)
    else:
        roles = rolesForPermissionOn(permission, object)
        return user.allowed(object, roles)
