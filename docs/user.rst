.. admonition:: GitHub-only

    WARNING: If you are reading this on GitHub, DON'T!
    Read the documentation at `docs.plone.org <http://docs.plone.org/develop/plone.api/docs/user.html>`_
    so you have working references and proper formatting.


.. module:: plone

.. _chapter_users:

Users
=====


.. _user_create_example:

Create user
-----------

To create a new user, use :meth:`api.user.create`.
If your portal is configured to use emails as usernames, you just need to pass in the email of the new user.

.. invisible-code-block: python

    from plone import api
    from plone.api.exc import InvalidParameterError
    try:
        api.portal.set_registry_record('plone.use_email_as_login', True)
    except InvalidParameterError:
        portal = api.portal.get()
        portal.portal_properties.site_properties.use_email_as_login = True

.. code-block:: python

    from plone import api
    user = api.user.create(email='alice@plone.org')

.. invisible-code-block: python

    self.assertEqual(user.id, 'alice@plone.org')
    self.assertEqual(user.getProperty('email'), 'alice@plone.org')


Otherwise, you also need to pass in the username of the new user.

.. invisible-code-block: python

    try:
        api.portal.set_registry_record('plone.use_email_as_login', False)
    except InvalidParameterError:
        portal = api.portal.get()
        portal.portal_properties.site_properties.use_email_as_login = False

.. code-block:: python

    user = api.user.create(email='jane@plone.org', username='jane')

.. invisible-code-block: python

    self.assertEqual(user.id, 'jane')
    self.assertEqual(user.getProperty('email'), 'jane@plone.org')


To set user properties when creating a new user, pass in a properties dict.

.. code-block:: python

    properties = dict(
        fullname='Bob',
        location='Munich',
    )
    user = api.user.create(
        username='bob',
        email='bob@plone.org',
        properties=properties,
    )

.. invisible-code-block: python

    self.assertEqual(user.getProperty('fullname'), 'Bob')
    self.assertEqual(user.getProperty('location'), 'Munich')


Besides user properties you can also specify a password for the new user.
Otherwise a random 8-character alphanumeric password will be generated.

.. code-block:: python

    user = api.user.create(
        username='noob',
        email='noob@plone.org',
        password='secret',
    )


.. _user_get_example:

Get user
--------

You can get a user with :meth:`api.user.get`.

.. code-block:: python

    from plone import api
    user = api.user.get(username='bob')

.. invisible-code-block: python

    self.assertEqual(user.id, 'bob')

User properties
---------------

Users have various properties set on them.
This is how you get and set them, using the underlying APIs:

.. code-block:: python

    from plone import api
    user = api.user.get(username='bob')
    user.setMemberProperties(mapping={ 'location': 'Neverland', })
    location = user.getProperty('location')

.. invisible-code-block: python

    self.assertEqual(location, 'Neverland')


.. _user_get_current_example:

Get currently logged-in user
----------------------------

Getting the currently logged-in user is easy with :meth:`api.user.get_current`.

.. code-block:: python

    from plone import api
    current = api.user.get_current()

.. invisible-code-block: python

    self.assertEqual(current.id, 'test_user_1_')


.. _user_is_anonymous_example:

Check if current user is anonymous
----------------------------------

Sometimes you need to trigger or display some piece of information only for logged-in users.
It's easy to use :meth:`api.user.is_anonymous` to do a basic check for it.

.. code-block:: python

    from plone import api
    if not api.user.is_anonymous():
        trigger = False
    trigger = True

.. invisible-code-block: python

    self.assertTrue(trigger)


.. _user_get_all_users_example:

Get all users
-------------

Get all users in your portal with :meth:`api.user.get_users`.

.. code-block:: python

    from plone import api
    users = api.user.get_users()

.. invisible-code-block: python

    self.assertTrue('test_user_1_' in [user.id for user in users])


.. _user_get_groups_users_example:

Get group's users
-----------------

If you set the `groupname` parameter, then :meth:`api.user.get_users` will return only users that are members of this group.

.. invisible-code-block: python

    api.group.create(groupname='staff')
    api.group.add_user(username='jane', groupname='staff')

.. code-block:: python

    from plone import api
    users = api.user.get_users(groupname='staff')

.. invisible-code-block: python

    self.assertEqual(users[0].id, 'jane')


.. _user_delete_example:

Delete user
-----------

To delete a user, use :meth:`api.user.delete` and pass in either the username or the user object you want to delete.

.. code-block:: python

    from plone import api
    api.user.create(username='unwanted', email='unwanted@example.org')
    api.user.delete(username='unwanted')


.. invisible-code-block: python

    self.assertEqual(api.user.get(username='unwanted'), None)

.. code-block:: python

    unwanted = api.user.create(username='unwanted', email='unwanted@example.org')
    api.user.delete(user=unwanted)

.. invisible-code-block: python

    self.assertEqual(api.user.get(username='unwanted'), None)


.. _user_get_roles_example:

Get user roles
----------------

The :meth:`api.user.get_roles` method is used for getting a user's roles.
By default it returns site-wide roles.

.. code-block:: python

    from plone import api
    roles = api.user.get_roles(username='jane')

.. invisible-code-block: python

    self.assertEqual(set(roles), set(['Member','Authenticated']))


If you pass in a content object, it will return local roles of the user in that particular context.

.. code-block:: python

    from plone import api
    portal = api.portal.get()
    blog = api.content.create(container=portal, type='Document', id='blog', title='My blog')
    roles = api.user.get_roles(username='jane', obj=portal['blog'])

.. invisible-code-block: python

    self.assertEqual(set(roles), set(['Member','Authenticated']))


.. _user_get_permissions_example:

Get user permissions
--------------------

The :meth:`api.user.get_permissions` method is used for getting user's permissions.
By default it returns site root permissions.

.. code-block:: python

    from plone import api
    mike = api.user.create(email='mike@plone.org', username='mike')
    permissions = api.user.get_permissions(username='mike')

.. invisible-code-block: python

    PERMISSIONS = {
        'View': True,
        'Manage portal': False,
        'Modify portal content': False,
        'Access contents information': True,
    }

    for k, v in PERMISSIONS.items():
        self.assertTrue(v == api.user.get_permissions(username='mike').get(k, None))
        self.assertTrue(v == api.user.get_permissions(user=mike).get(k, None))


If you pass in a content object, it will return local permissions of the user in that particular context.

.. code-block:: python

    from plone import api
    portal = api.portal.get()
    folder = api.content.create(container=portal, type='Folder', id='folder_two', title='Folder Two')
    permissions = api.user.get_permissions(username='mike', obj=portal['folder_two'])

.. invisible-code-block: python

    PERMISSIONS = {
        'View': False,
        'Manage portal': False,
        'Modify portal content': False,
        'Access contents information': False,
    }

    for k, v in PERMISSIONS.items():
        self.assertTrue(v == api.user.get_permissions(username='mike', obj=portal['folder_two']).get(k, None))
        self.assertTrue(v == api.user.get_permissions(user=mike, obj=portal['folder_two']).get(k, None))


.. _user_has_permission_example:

Check user permission
----------------------

Instead of getting all user permissions, you can check a single permission using the :meth:`api.user.has_permission` method.
By default it checks the permission on the site root.

.. code-block:: python

    from plone import api
    adam = api.user.create(email='adam@plone.org', username='adam')
    can_view = api.user.has_permission('View', username='adam')

.. invisible-code-block: python

   self.assertTrue(can_view)


If you pass in a content object, it will check the permission in that particular context.

.. code-block:: python

    from plone import api
    portal = api.portal.get()
    folder = api.content.create(container=portal, type='Folder', id='folder_hp', title='Folder')
    can_view = api.user.has_permission('View', username='adam', obj=folder)

.. invisible-code-block: python

   self.assertFalse(can_view)


.. _user_grant_roles_example:

Grant roles to user
-------------------

The :meth:`api.user.grant_roles` allows us to grant a list of roles to the user.

.. code-block:: python

    from plone import api
    api.user.grant_roles(username='jane',
        roles=['Reviewer', 'SiteAdministrator']
    )

.. invisible-code-block: python

    EXPECTED_ROLES_SITE = ['Member', 'Reviewer', 'SiteAdministrator', 'Authenticated']
    roles = api.user.get_roles(username='jane')
    self.assertEqual(set(EXPECTED_ROLES_SITE), set(roles))


If you pass a content object or folder,
the roles are granted only on that context and not site-wide.
But all site-wide roles will also be returned by :meth:`api.user.get_roles` for this user on the given context.

.. code-block:: python

    from plone import api
    folder = api.content.create(container=portal, type='Folder', id='folder_one', title='Folder One')
    api.user.grant_roles(username='jane',
        roles=['Editor', 'Contributor'],
        obj=portal['folder_one']
    )

.. invisible-code-block: python

    EXPECTED_ROLES_CONTEXT = EXPECTED_ROLES_SITE + ['Editor', 'Contributor']
    roles = api.user.get_roles(username='jane', obj=portal['folder_one'])
    self.assertEqual(set(EXPECTED_ROLES_CONTEXT), set(roles))
    roles = api.user.get_roles(username='jane')
    self.assertEqual(set(EXPECTED_ROLES_SITE), set(roles))


.. _user_revoke_roles_example:

Revoke roles from user
----------------------

The :meth:`api.user.revoke_roles` allows us to revoke a list of roles from the user.

.. code-block:: python

    from plone import api
    api.user.revoke_roles(username='jane', roles=['SiteAdministrator'])

.. invisible-code-block: python

    EXPECTED_ROLES_SITE = ['Member', 'Authenticated', 'Reviewer']
    roles = api.user.get_roles(username='jane')
    self.assertEqual(set(EXPECTED_ROLES_SITE), set(roles))


If you pass a context object the local roles for that context will be removed.

.. code-block:: python

    from plone import api
    folder = api.content.create(
        container=portal,
        type='Folder',
        id='folder_three',
        title='Folder Three'
    )
    api.user.grant_roles(
        username='jane',
        roles=['Editor', 'Contributor'],
        obj=portal['folder_three'],
    )
    api.user.revoke_roles(
        username='jane',
        roles=['Editor'],
        obj=portal['folder_three'],
    )

.. invisible-code-block: python

    EXPECTED_ROLES_CONTEXT = EXPECTED_ROLES_SITE + ['Contributor']
    roles = api.user.get_roles(username='jane', obj=portal['folder_three'])
    self.assertEqual(set(EXPECTED_ROLES_CONTEXT), set(roles))

Further reading
---------------

For more information on possible flags and usage options please see the full :ref:`plone-api-user` specification.
