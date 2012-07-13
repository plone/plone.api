.. module:: plone

.. _chapter_groups:

Groups
======

.. _group_create_example:

Create group
------------

To create a new portal group, use :meth:`api.group.create`.

.. code-block:: python

    from plone import api
    group = api.group.create(groupname='staff')

.. invisible-code-block:: python

    self.assertEquals(group.id, 'staff')

When creating groups ``title``, ``description``, ``roles`` and ``groups`` are optional.

.. code-block:: python

    from plone import api

    group = api.group.create(
        groupname='board_members',
        title='Board members',
        description='Just a description',
        roles=['Readers', ],
        groups=['Site Administrators', ]
    )

.. invisible-code-block:: python

    self.assertEquals(group.id, 'board_members')
    self.assertEquals(group.getProperty('title'), 'Board members')
    self.assertEquals(group.getProperty('description'), 'Just a description')
    assert 'Readers' in group.getRoles()
    assert 'Site Administrators' in group.getMemberIds()

.. _group_get_example:

Get group
---------

To get a group by it's name, use :meth:`api.group.get`.

.. code-block:: python

    from plone import api
    group = api.group.get(groupname='staff')

.. invisible-code-block:: python

    self.assertEquals(group.id, 'staff')


.. _group_edit:

Editing a group
---------------

Groups can be edited by using the ``group_tool``. In this example the ``title``,
``description`` and ``roles`` are updated for the group 'Staff'.

.. code-block:: python

    group_tool = api.portal.get_tool(name='portal_groups')
    group_tool.editGroup(
        'staff',
        roles=['Editor', 'Reader'],
        title='Staff',
        description='Just a description',
    )

    group = api.group.get(groupname='staff')

    title = group.getProperty('title')
    description = group.getProperty('description')
    roles = group.getRoles()

.. invisible-code-block:: python

    self.assertEqual(title, 'Staff')
    self.assertEqual(description, 'Just a description')
    assert 'Editor' in roles
    assert 'Reader' in roles


Get all groups
--------------

You can also get all groups, by using :meth:`api.group.get_all`.

.. code-block:: python

    from plone import api
    groups = api.group.get_all()

.. invisible-code-block:: python

    self.assertEquals(groups[0].id, 'Administrators')


.. _group_delete_example:

Delete group
------------

To delete a group, use :meth:`api.group.delete` and pass in either the groupname
or the group object you want to delete.

.. code-block:: python

    from plone import api
    api.group.create(groupname='unwanted')
    api.group.delete(groupname='unwanted')

.. invisible-code-block:: python

    assert not api.group.get(groupname='unwanted')

.. code-block:: python

    unwanted = api.group.create(groupname='unwanted')
    api.group.delete(group=unwanted)

.. invisible-code-block:: python

    assert not api.group.get(groupname='unwanted')

Adding user to group
--------------------

The ``add_user`` method accepts either the groupname or the group object of the target group and
the username or the user object you want to add to the group.

.. code-block:: python

    from plone import api

    api.user.create(email='jane@plone.org', username='jane')
    api.user.create(email='bob@plone.org', username='bob')

    api.group.add_user(groupname='staff', username='bob')

    user = api.user.get(username='jane')
    group = api.group.get(groupname='staff')
    api.group.add_user(group=group, user=user)

.. invisible-code-block:: python

    assert 'staff' in api.user.get_groups(username='bob')
    assert 'staff' in api.user.get_groups(username='jane')

.. _delete_user_from_group_example:

Deleting user from group
------------------------

The ``delete_user`` method accepts either the groupname or the group object of the target
group and either the username or the user object you want to remove from the group.

.. code-block:: python

    from plone import api
    api.group.delete_user(groupname='staff', username='bob')

    group = api.group.get(groupname='staff')
    user = api.user.get(username='jane')
    api.group.delete_user( group=group, user=user)

.. invisible-code-block:: python

    assert 'staff' not in api.user.get_groups(username='bob')
    assert 'staff' not in api.user.get_groups(username='jane')
