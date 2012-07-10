from plone import api

def create(email=None, username=None, password=None, properties=None, *args):
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
    :Example: :ref:`create_user_example`
    """
    if args:
        raise ValueError('Positional arguments are not allowed!')

    if not email:
        raise ValueError

    site = api.get_site()
    use_email_as_username = site.portal_properties.use_email_as_username
    if not use_email_as_username and not username:
        raise ValueError

    raise NotImplementedError


def get(username=None, *args):
    """Get a user.

    :param username: [required] Username of the user we want to get.
    :type username: string
    :returns: User
    :rtype: MemberData object
    :Example: :ref:`get_user_example`
    """

    if args:
        raise ValueError('Positional arguments are not allowed!')

    if not username:
        raise ValueError

    raise NotImplementedError


def get_current():
    """Get the currently logged-in user.

    :returns: Currently logged-in user
    :rtype: MemberData object
    :Example: :ref:`get_current_user_example`
    """
    raise NotImplementedError


def get_all():
    """Returns all users.

    :returns: All users
    :rtype: List of MemberData objects
    :Example: :ref:`get_all_users_example`
    """
    raise NotImplementedError


def delete(username=None, user=None, *args):
    """Delete a user.

    Arguments ``username`` and ``user`` are mutually exclusive. You can either
    set one or the other, but not both.

    :param username: Username of the to be deleted user.
    :type username: string
    :param user: User object to be deleted.
    :type user: MemberData object
    :Example: :ref:`delete_user_example`
    """

    if args:
        raise ValueError('Positional arguments are not allowed!')

    if not username and not user:
        raise ValueError

    if username and user:
        raise ValueError


def change_password(username=None, user=None, password=None, *args):
    """Change the user's password.

    Arguments ``username`` and ``user`` are mutually exclusive. You can either
    set one or the other, but not both.

    :param username: Username of the user for which to change the
        password for.
    :type username: string
    :param user: User for which to change the password for.
    :type user: MemberData object
    :param password: New password for the user. If it's not set we generate
        a random 8-char alpha-numeric one.
    :type password: string
    :Example: :ref:`change_password_example`
    """

    if args:
        raise ValueError('Positional arguments are not allowed!')

    if not username and not user:
        raise ValueError

    if username and user:
        raise ValueError

    raise NotImplementedError


def get_property(username=None, user=None, name=None, *args):
    """Get a user's property.

    Arguments ``username`` and ``user`` are mutually exclusive. You can either
    set one or the other, but not both.

    :param username: Username of the user for which to get property for
    :type username: string
    :param user: User for which to get property for.
    :type user: MemberData object
    :param name: Name of the property to return
    :type name: string
    :returns: Property's value
    :rtype: string, tuple, DateTime, etc.
    :Example: :ref:`get_user_property_example`
    """

    if args:
        raise ValueError('Positional arguments are not allowed!')

    if not username and not user:
        raise ValueError

    if username and user:
        raise ValueError

    if not name:
        raise ValueError

    raise NotImplementedError


def set_property(username=None, user=None, name=None, value=None, *args):
    """Set a user's property.

    Arguments ``username`` and ``user`` are mutually exclusive. You can either
    set one or the other, but not both.

    :param username: Username of the user for which to modify the property.
    :type username: string
    :param user: User for which to modify the property.
    :type user: MemberData object
    :param name: Name of the property to modify.
    :type name: string
    :param value: Value to set to the property.
    :type value: string, tuple, DateTime, etc.
    :Example: :ref:`set_user_property_example`
    """

    if args:
        raise ValueError('Positional arguments are not allowed!')

    if not username and not user:
        raise ValueError

    if username and user:
        raise ValueError

    if not name:
        raise ValueError

    if not value:
        raise ValueError

    raise NotImplementedError


def get_groups(username=None, user=None, *args):
    """Get a list of groups that this user is a member of.

    Arguments ``username`` and ``user`` are mutually exclusive. You can either
    set one or the other, but not both.

    :param username: Username of the user for which to return groups.
    :type username: string
    :param user: User for which to return groups.
    :type user: MemberData object
    :returns: List of group names of groups this user is member of.
    :rtype: List of strings
    :Example: :ref:`get_groups_for_user_example`
    """

    if args:
        raise ValueError('Positional arguments are not allowed!')

    if not username and not user:
        raise ValueError

    if username and user:
        raise ValueError

    raise NotImplementedError


def join_group(username=None, user=None, groupname=None, group=None, *args):
    """Add the user to a group.

    Arguments ``username`` and ``user`` are mutually exclusive. You can either
    set one or the other, but not both.

    Arguments ``groupname`` and ``group`` are also mutually exclusive. You can
    either set one or the other, but not both.

    :param username: Username of the user to join the group.
    :type username: string
    :param user: User to join the group.
    :type user: MemberData object
    :param groupname: Group name of the group to which to join the user.
    :type groupname: string
    :param group: Group to which to join the user.
    :type group: GroupData object
    :Example: :ref:`add_user_to_group_example`
    """

    if args:
        raise ValueError('Positional arguments are not allowed!')

    if not username and not user:
        raise ValueError

    if username and user:
        raise ValueError

    if not groupname and not group:
        raise ValueError

    if groupname and group:
        raise ValueError

    raise NotImplementedError


def leave_group(username=None, user=None, groupname=None, group=None, *args):
    """Remove the user from a group.

    Arguments ``username`` and ``user`` are mutually exclusive. You can either
    set one or the other, but not both.

    Arguments ``groupname`` and ``group`` are mutually exclusive. You can
    either set one or the other, but not both.

    :param username: Username of the user to leave the group.
    :type username: string
    :param user: User to leave the group.
    :type user: MemberData object
    :param groupname: Group name of the group from which to remove the user.
    :type groupname: string
    :param group: Group from which to remove the user.
    :type group: GroupData object
    :Example: :ref:`remove_user_from_group_example`
    """

    if args:
        raise ValueError('Positional arguments are not allowed!')

    if not username and not user:
        raise ValueError

    if username and user:
        raise ValueError

    if not groupname and not group:
        raise ValueError

    if groupname and group:
        raise ValueError

    raise NotImplementedError


def is_anonymous():
    """Check if the currently logged-in user is anonymous.

    :returns: True if the current user is anonymous, False otherwise.
    :rtype: bool
    :Example: :ref:`is_anonymous_example`
    """
    raise NotImplementedError


def has_role(role=None, username=None, user=None, *args):
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
    :Example: :ref:`has_role_example`
    """
    if args:
        raise ValueError('Positional arguments are not allowed!')

    if not role:
        raise ValueError

    if username and user:
        raise ValueError

    raise NotImplementedError


def has_permission(permission=None, username=None, user=None, *args):
    """Check if the user has the specified permission.

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
    :returns: True if user has the specified permission, False otherwise.
    :rtype: bool
    :Example: :ref:`has_permission_example`
    """
    if args:
        raise ValueError('Positional arguments are not allowed!')

    if not permission:
        ValueError

    if username and user:
        raise ValueError

    raise NotImplementedError
