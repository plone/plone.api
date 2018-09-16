.. admonition:: GitHub-only

    WARNING: If you are reading this on GitHub, DON'T!
    Read the documentation at `docs.plone.org <http://docs.plone.org/develop/plone.api/docs/group.html>`_
    so you have working references and proper formatting.


.. module:: plone

.. _chapter_groups:

Groups
======



.. _group_create_example:

Create group
------------

To create a new group, use :meth:`api.group.create`.

.. code-block:: python

    from plone import api
    group = api.group.create(groupname='staff')

.. invisible-code-block: python

    self.assertEqual(group.id, 'staff')

When you create groups, ``title``, ``description``, ``roles`` and ``groups`` are optional.

.. code-block:: python

    from plone import api

    group = api.group.create(
        groupname='board_members',
        title='Board members',
        description='Just a description',
        roles=['Reader', ],
        groups=['Site Administrators', ],
    )

.. invisible-code-block: python

    self.assertEqual(group.id, 'board_members')
    self.assertEqual(group.getProperty('title'), 'Board members')
    self.assertEqual(group.getProperty('description'), 'Just a description')
    self.assertTrue('Reader' in group.getRoles())
    self.assertTrue('Site Administrators' in group.getMemberIds())


.. _group_get_example:

Get group
---------

To get a group by its name, use :meth:`api.group.get`.

.. code-block:: python

    from plone import api
    group = api.group.get(groupname='staff')

.. invisible-code-block: python

    self.assertEqual(group.id, 'staff')


.. _group_edit_example:

Editing a group
---------------

Groups can be edited by using the ``group_tool``.
In this example, the ``title``, ``description`` and ``roles`` are updated for the group 'Staff'.

.. code-block:: python

    from plone import api
    group_tool = api.portal.get_tool(name='portal_groups')
    group_tool.editGroup(
        'staff',
        roles=['Editor', 'Reader'],
        title='Staff',
        description='Just a description',
    )

.. invisible-code-block: python

    group = api.group.get(groupname='staff')

    title = group.getProperty('title')
    description = group.getProperty('description')
    roles = group.getRoles()

    self.assertEqual(title, 'Staff')
    self.assertEqual(description, 'Just a description')
    self.assertTrue('Editor' in roles)
    self.assertTrue('Reader' in roles)


.. _group_get_all_groups_example:

Get all groups
--------------

You can also get all groups by using :meth:`api.group.get_groups`.

.. code-block:: python

    from plone import api
    groups = api.group.get_groups()

.. invisible-code-block: python

    self.assertEqual(groups[0].id, 'Administrators')


.. _group_get_users_groups_example:

Get user's groups
-----------------

Groups may be filtered by member. By passing the ``username`` parameter,
:meth:`api.group.get_groups` will return only the groups the user belongs to.

.. invisible-code-block: python

    api.user.create(email='jane@plone.org', username='jane')
    api.group.add_user(username='jane', groupname='staff')
    api.group.add_user(username='jane', groupname='Reviewers')

.. code-block:: python

    from plone import api
    user = api.user.get(username='jane')
    groups = api.group.get_groups(username='jane')

.. invisible-code-block: python

    group_list = [g.id for g in groups]
    import six
    if six.PY2:
        assertCountEqual = self.assertItemsEqual
    else:
        assertCountEqual = self.assertCountEqual

    assertCountEqual(
        group_list,
        ['Reviewers', 'AuthenticatedUsers', 'staff'],
    )

You can also pass the user directly to :meth:`api.group.get_groups`:

    from plone import api
    user = api.user.get(username='jane')
    groups = api.group.get_groups(user=user)

.. invisible-code-block: python

    group_list = [g.id for g in groups]
    assertCountEqual(
        group_list,
        ['Reviewers', 'AuthenticatedUsers', 'staff'],
    )

Get group members
-----------------

Use the :meth:`api.user.get_users` method to get all the users that are members of a group.


.. code-block:: python

    from plone import api
    members = api.user.get_users(groupname='staff')

.. invisible-code-block: python

    self.assertEqual(members[0].id, 'jane')


.. _group_delete_example:

Delete group
------------

To delete a group, use :meth:`api.group.delete` and pass in either the groupname or the group object you want to delete.

.. code-block:: python

    from plone import api
    api.group.create(groupname='unwanted')
    api.group.delete(groupname='unwanted')

.. invisible-code-block: python

    self.assertEqual(api.group.get(groupname='unwanted'), None)

.. code-block:: python

    unwanted = api.group.create(groupname='unwanted')
    api.group.delete(group=unwanted)

.. invisible-code-block: python

    self.assertEqual(api.group.get(groupname='unwanted'), None)


.. _group_add_user_example:

Adding user to group
--------------------

To add a user to a group, use the :meth:`api.group.add_user` method.
This method accepts either the groupname or the group object for the target group and the username or the user object you want to add to the group.

.. code-block:: python

    from plone import api

    api.user.create(email='bob@plone.org', username='bob')
    api.group.add_user(groupname='staff', username='bob')

.. invisible-code-block: python

    self.assertTrue(
        'staff' in [g.id for g in api.group.get_groups(username='bob')]
    )


.. _group_remove_user_example:

Removing user from group
------------------------

To remove a user from a group, use the :meth:`api.group.remove_user` method.
This also accepts either the groupname or the group object for the target group and either the username or the user object you want to remove from the group.

.. code-block:: python

    from plone import api
    api.group.remove_user(groupname='staff', username='bob')


.. invisible-code-block: python

    self.assertFalse('staff' in [g.id for g in api.group.get_groups(username='bob')])


.. _group_get_roles_example:

Get group roles
---------------

To find the roles assigned to a group, use the :meth:`api.group.get_roles` method.
By default it returns site-wide roles.

.. code-block:: python

    from plone import api
    roles = api.group.get_roles(groupname='staff')

.. invisible-code-block: python

    EXPECTED_SITE_ROLES = ['Authenticated', 'Editor', 'Reader']
    self.assertEqual(set(EXPECTED_SITE_ROLES), set(roles))

If you pass in a content object, it will return the local roles of the group in that particular context.

.. code-block:: python

    from plone import api
    portal = api.portal.get()
    folder = api.content.create(
        container=portal,
        type='Folder',
        id='folder_four',
        title='Folder Four',
    )
    roles = api.group.get_roles(groupname='staff', obj=portal['folder_four'])

.. invisible-code-block: python

    self.assertEqual(set(EXPECTED_SITE_ROLES), set(roles))

If you pass in a content object and `inherit=False`, it will return only the local roles of the group on that particular object and ignore global roles.

.. code-block:: python

    api.group.grant_roles(
        groupname='staff', roles=['Contributor'], obj=portal['folder_four'])

    roles = api.group.get_roles(
        groupname='staff', obj=portal['folder_four'], inherit=False)

.. invisible-code-block: python

    EXPECTED_OBJ_ROLES = ['Contributor']
    self.assertEqual(set(EXPECTED_OBJ_ROLES), set(roles))


.. _group_grant_roles_example:

Grant roles to group
--------------------

To grant roles to a group, use the :meth:`api.group.grant_roles` method.
By default, roles are granted site-wide.

.. code-block:: python

    from plone import api
    api.group.grant_roles(
        groupname='staff',
        roles=['Reviewer, SiteAdministrator'],
    )

.. invisible-code-block: python

    EXPECTED_SITE_ROLES = ['Authenticated', 'Editor', 'Reader', 'Reviewer, SiteAdministrator']
    roles = api.group.get_roles(groupname='staff')
    self.assertEqual(set(EXPECTED_SITE_ROLES), set(roles))


If you pass in a content object, roles will be assigned in that particular context.

.. code-block:: python

    from plone import api
    portal = api.portal.get()
    folder = api.content.create(
        container=portal, type='Folder', id='folder_five', title='Folder Five')
    api.group.grant_roles(
        groupname='staff', roles=['Contributor'], obj=portal['folder_five'])

.. invisible-code-block: python

    EXPECTED_CONTEXT_ROLES = EXPECTED_SITE_ROLES + ['Contributor']
    roles = api.group.get_roles(groupname='staff', obj=portal['folder_five'], inherit=False)
    self.assertEqual(set(['Contributor']), set(roles))
    roles = api.group.get_roles(groupname='staff', obj=portal['folder_five'])
    self.assertEqual(set(EXPECTED_CONTEXT_ROLES), set(roles))


.. _group_revoke_roles_example:

Revoke roles from group
-----------------------

To revoke roles already granted to a group, use the :meth:`api.group.revoke_roles` method.

.. code-block:: python

    from plone import api
    api.group.revoke_roles(
        groupname='staff', roles=['Reviewer, SiteAdministrator'])

.. invisible-code-block: python

    EXPECTED_SITE_ROLES = ['Authenticated', 'Editor', 'Reader']
    roles = api.group.get_roles(groupname='staff')
    self.assertEqual(set(EXPECTED_SITE_ROLES), set(roles))


If you pass in a content object, it will revoke roles granted in that particular context.

.. invisible-code-block: python

    EXPECTED_CONTEXT_ROLES = ['Contributor']
    roles = api.group.get_roles(groupname='staff', obj=portal['folder_five'], inherit=False)
    self.assertEqual(['Contributor'], roles)


.. code-block:: python

    from plone import api
    api.group.revoke_roles(
        groupname='staff', roles=['Contributor'], obj=portal['folder_five'])


.. invisible-code-block: python

    EXPECTED_CONTEXT_ROLES = []
    roles = api.group.get_roles(groupname='staff', obj=portal['folder_five'], inherit=False)
    self.assertEqual(set(EXPECTED_CONTEXT_ROLES), set(roles))


Further reading
---------------

For more information on possible flags and complete options please see the full :ref:`plone-api-group` specification.
