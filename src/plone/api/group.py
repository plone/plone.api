

def create(groupname=None, *args):
    """Creates a group.

    :param groupname: [required] Name of the new group.
    :type groupname: string
    :returns: Newly created group
    :rtype: GroupData object
    :Example: :ref:`create_group_example`
    """

    if args:
        raise ValueError('Positional arguments are not allowed!')

    if not groupname:
        raise ValueError('You have to pass the groupname parameter!')

    pass


def get(groupname=None, *args):
    """Returns a group.

    :param groupname: [required] Name of the group we want to get.
    :type groupname: string
    :returns: Group
    :rtype: GroupData object
    :Example: :ref:`get_group_example`
    """

    if args:
        raise ValueError('Positional arguments are not allowed!')

    if not groupname:
        raise ValueError('You have to pass the groupname parameter!')

    pass


def delete(groupname=None, group=None, *args):
    """Deletes a group.

    Arguments ``groupname`` and ``group`` are mutually exclusive. You can
    either set one or the other, but not both.

    :param groupname: Name of the group to be deleted.
    :type groupname: string
    :param group: Group object to be deleted.
    :type group: GroupData object
    :Example: :ref:`delete_group_example`
    """

    if args:
        raise ValueError('Positional arguments are not allowed!')

    if not groupname and not group:
        raise ValueError

    if groupname and group:
        raise ValueError

    pass
