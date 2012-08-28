.. line-block::

    WARNING: If you are reading this on GitHub, DON'T! Read it on ReadTheDocs:
    http://ploneapi.readthedocs.org/en/latest/groups.html so you have working
    references and proper formatting.


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


.. _group_edit_example:

Editing a group
---------------

Groups can be edited by using the ``group_tool``. In this example the ``title``,
``description`` and ``roles`` are updated for the group 'Staff'.

.. code-block:: python

    from plone import api
    group_tool = api.portal.get_tool(name='portal_groups')
    group_tool.editGroup(
        'staff',
        roles=['Editor', 'Reader'],
        title='Staff',
        description='Just a description',
    )

.. invisible-code-block:: python

    group = api.group.get(groupname='staff')

    title = group.getProperty('title')
    description = group.getProperty('description')
    roles = group.getRoles()

    self.assertEqual(title, 'Staff')
    self.assertEqual(description, 'Just a description')
    assert 'Editor' in roles
    assert 'Reader' in roles


.. _group_get_all_groups_example:

Get all groups
--------------

You can also get all groups, by using :meth:`api.group.get_groups`.

.. code-block:: python

    from plone import api
    groups = api.group.get_groups()

.. invisible-code-block:: python

    self.assertEquals(groups[0].id, 'Administrators')


.. _group_get_users_groups_example:

Get user's groups
-----------------

If you pass in a `user`, then :meth:`api.group.get_groups` will return groups
that the user is member of.

.. invisible-code-block:: python

    api.user.create(email='jane@plone.org', username='jane')
    api.group.add_user(username='jane', groupname='staff')
    api.group.add_user(username='jane', groupname='Reviewers')

.. code-block:: python

    from plone import api
    user = api.user.get(username='jane')
    groups = api.group.get_groups(username='jane')

.. invisible-code-block:: python

    self.assertEquals(groups[0].id, 'Reviewers')
    self.assertEquals(groups[1].id, 'AuthenticatedUsers')
    self.assertEquals(groups[2].id, 'staff')


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


.. _group_add_user_example:

Adding user to group
--------------------

The :meth:`api.group.add_user` method accepts either the groupname or the group
object of the target group and the username or the user object you want to add
to the group.

.. code-block:: python

    from plone import api

    api.user.create(email='bob@plone.org', username='bob')
    api.group.add_user(groupname='staff', username='bob')

.. invisible-code-block:: python

    assert 'staff' in [g.id for g in api.group.get_groups(username='bob')]


.. _group_remove_user_example:

Removing user from group
------------------------

The :meth:`api.group.remove_user` method accepts either the groupname or the
group object of the target group and either the username or the user object you
want to remove from the group.

.. code-block:: python

    from plone import api
    api.group.remove_user(groupname='staff', username='bob')


.. invisible-code-block:: python

    assert 'staff' not in [g.id for g in api.group.get_groups(username='bob')]
