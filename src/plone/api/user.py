

def create(email=None, username=None, password=None, properties=None, *args):
    """Creates a user.

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

    use_email_as_username = site.portal_properties.use_email_as_username
    if not use_email_as_username and not username:
        raise ValueError

    pass


def get(username=None, *args):
    """Returns a user.

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

    pass


def get_current():
    """Returns the currently logged-in user.

    :returns: Currently logged-in user
    :rtype: MemberData object
    :Example: :ref:`get_current_user_example`
    """
    pass


def delete(username=None, user=None, *args):
    """Deletes a user.

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
    """Changes a user's password.

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

    pass


def get_property(username=None, user=None, name=None, *args):
    """Returns a user's property.

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

    pass


def set_property(username=None, user=None, name=None, value=None, *args):
    """Returns a user's property.

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

    pass


def get_groups(username=None, user=None, *args):
    """Returns a list of groups that this user is a member of.

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

    pass


def join_group(username=None, user=None, groupname=None, group=None, *args):
    """Join a user to a group.

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

    pass


def leave_group(username=None, user=None, groupname=None, group=None, *args):
    """Remove the user from a group.

    Arguments ``username`` and ``user`` are mutually exclusive. You can either
    set one or the other, but not both.

    Arguments ``groupname`` and ``group`` are mutually exclusive. You can either
    set one or the other, but not both.

    :param username: Username of the user to leave the group.
    :type username: string
    :param user: User to leave the group.
    :type user: MemberData object
    :param groupname: Group name of the group from which to un-join the user.
    :type groupname: string
    :param group: Group from which to un-join the user.
    :type group: GroupData object
    :Example: :ref:`drop_user_from_group_example`
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

    pass
