.. line-block::

    WARNING: If you are reading this on GitHub, DON'T! Read it on ReadTheDocs:
    http://ploneapi.readthedocs.org/en/latest/users.html so you have working
    references and proper formatting.


.. module:: plone

.. _chapter_users:

Users
=====

.. _user_create_example:

Create user
-----------

To create a new user, use :meth:`api.user.create`. If your portal is
configured to use emails as usernames, you just need to pass in the email of
the new user.

.. invisible-code-block:: python

    from plone import api
    portal = api.portal.get()
    portal.portal_properties.site_properties.use_email_as_login = True

.. code-block:: python

    from plone import api
    user = api.user.create(email='alice@plone.org')

.. invisible-code-block:: python

    self.assertEquals(user.id, 'alice@plone.org')
    self.assertEquals(user.getProperty('email'), 'alice@plone.org')


Otherwise, you also need to pass in the username of the new user.

.. invisible-code-block:: python

    portal.portal_properties.site_properties.use_email_as_login = False

.. code-block:: python

    user = api.user.create(email='jane@plone.org', username='jane')

.. invisible-code-block:: python

    self.assertEquals(user.id, 'jane')
    self.assertEquals(user.getProperty('email'), 'jane@plone.org')


To set user properties when creating a new user, pass in a properties dict.

.. code-block:: python

    properties = dict(
        fullname='Bob',
        location='Munich',
    )
    user = api.user.create(
        username='bob',
        email='bob@plone.org',
        properties=properties
    )

.. invisible-code-block:: python

    self.assertEquals(user.getProperty('fullname'), 'Bob')
    self.assertEquals(user.getProperty('location'), 'Munich')


Besides user properties you can also specify a password for the new user.
Otherwise a random 8-char alphanumeric password will be generated.

.. code-block:: python

    user = api.user.create(
        username='noob',
        email='noob@plone.org',
        password='secret'
    )


.. _user_get_example:

Get user
--------

You can get a user with :meth:`api.user.get`.

.. code-block:: python

    from plone import api
    user = api.user.get(username='bob')

.. invisible-code-block:: python

    self.assertEquals(user.id, 'bob')


.. _user_get_current_example:

Get currently logged-in user
----------------------------

Getting the currently logged-in user is easy with :meth:`api.user.get_current`.

.. code-block:: python

    from plone import api
    current = api.user.get_current()

.. invisible-code-block:: python

    self.assertEquals(current.id, 'test_user_1_')


.. _user_is_anonymous_example:

Check if current user is anonymous
----------------------------------

Sometimes you need to trigger or display some piece of information only for
logged-in users. It's easy to use :meth:`api.user.is_anonymous` to do a basic
check for it.

.. code-block:: python

    from plone import api
    if not api.user.is_anonymous():
        trigger = False
    trigger = True

.. invisible-code-block:: python

    self.assertTrue(trigger)


.. _user_get_all_users_example:

Get all users
-------------

Get all users in your portal with :meth:`api.user.get_users`.

.. code-block:: python

    from plone import api
    users = api.user.get_users()

.. invisible-code-block:: python

    self.assertTrue('test_user_1_' in [user.id for user in users])


.. _user_get_groups_users_example:

Get group's users
-----------------

If you set the `groupname` parameter, then :meth:`api.user.get_users` will
return only users that are members of this group.

.. invisible-code-block:: python

    api.group.create(groupname='staff')
    api.group.add_user(username='jane', groupname='staff')

.. code-block:: python

    from plone import api
    users = api.user.get_users(groupname='staff')

.. invisible-code-block:: python

    self.assertEquals(users[0].id, 'jane')


.. _user_delete_example:

Delete user
-----------

To delete a user, use :meth:`api.user.delete` and pass in either the username or
the user object you want to delete.

.. code-block:: python

    from plone import api
    api.user.create(username='unwanted', email='unwanted@example.org')
    api.user.delete(username='unwanted')


.. invisible-code-block:: python

    self.assertEqual(api.user.get(username='unwanted'), None)

.. code-block:: python

    unwanted = api.user.create(username='unwanted', email='unwanted@example.org')
    api.user.delete(user=unwanted)

.. invisible-code-block:: python

    self.assertEqual(api.user.get(username='unwanted'), None)


.. _user_get_roles_example:

Get user's roles
----------------

The :meth:`api.user.get_roles` method is used to getting user's roles.
By default it returns site-wide roles.

.. code-block:: python

    from plone import api
    roles = api.user.get_roles(username='jane')

.. invisible-code-block:: python

    self.assertEqual(set(roles), set(['Member','Authenticated']))


If you pass in a content object, it will return local roles of the user
in that particular context.

.. code-block:: python

    from plone import api
    portal = api.portal.get()
    roles = api.user.get_roles(username='staff', obj=portal['blog'])

.. invisible-code-block:: python

    self.assertEqual(set(roles), set(['Member','Authenticated','Owner']))


.. _user_get_permissions_example:

Get user permissions
--------------------

The :meth:`api.user.get_permissions` method is used to getting user's
permissions. By default it returns site-wide permissions.

.. code-block:: python

    from plone import api
    # permissions = api.user.get_permissions(username='jane')
    # Not implemented yet

If you pass in a content object, it will return local permissions of the user
in that particular context.

.. code-block:: python

    from plone import api
    portal = api.portal.get()
    # permissions = api.user.get_permissions(
    #    username='jane', obj=portal['blog'])
    # Not implemented yet


.. _user_grant_roles_example:

Grant roles to user
-------------------

The :meth:`api.user.grant_roles` allows us to grant a list of roles to the
user.

.. code-block:: python

    from plone import api
    # api.user.grant_roles(username='jane',
    #    roles=['Reviewer, SiteAdministrator'])
    # Not implemented yet


.. _user_revoke_roles_example:

Revoke roles from user
----------------------

The :meth:`api.user.revoke_roles` allows us to revoke a list of roles from the
user.

.. code-block:: python

    from plone import api
    # api.user.revoke_roles(username='jane',
    #    roles=['Reviewer, SiteAdministrator'])
    # Not implemented yet
