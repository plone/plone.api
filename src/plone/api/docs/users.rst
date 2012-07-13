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


.. _user_get_all_example:

Get all users
-------------

Get all users in your portal with :meth:`api.user.get_all`.

.. code-block:: python

    from plone import api
    users = api.user.get_all()

.. invisible-code-block:: python

    self.assertTrue('test_user_1_' in [user.id for user in users])


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


.. _user_has_role_example:

Check for role
--------------

Again on the security aspects, checking if a user has a certain role can be done
with :meth:`api.user.has_role`. If you omit the ``user`` parameter, the
currently logged-in user will be used.

.. code-block:: python

    from plone import api
    has_role = api.user.has_role(username='bob', role='Manager')

.. invisible-code-block:: python

    self.assertFalse(has_role)

When user is omitted the current user is used for role lookup.

.. code-block:: python

    from plone import api
    has_role = api.user.has_role(role='Manager')

.. invisible-code-block:: python

    self.assertTrue(has_role)

.. _user_has_permission_example:

Check for permission
--------------------

Likewise, you can also check if a user has a certain permission with
:meth:`api.user.has_permission`. Omitting the ``user`` parameter means the
currently logged-in user will be used.

.. code-block:: python

    from plone import api

    has_perm = api.user.has_permission(
        username='bob',
        permission='Manage portal content',
        object=api.portal.get()
    )

.. invisible-code-block:: python

    self.assertFalse(has_perm)

When user is omitted the current user is used for the permission check.

.. code-block:: python

    from plone import api
    has_perm = api.user.has_permission(
        permission='Manage portal content',
        object=api.portal.get()
    )

.. invisible-code-block:: python

    self.assertTrue(has_perm)

.. _get_groups_for_user_example:

Get groups that user is a member of
-----------------------------------

Use ``get_groups``, passing in either the username or the user object you want
to get groups for.

.. code-block:: python

    from plone import api
    api.group.add_user(groupname='Reviewers', username='bob')
    groups = api.user.get_groups(username='bob')

.. invisible-code-block:: python

    assert 'Reviewers' in groups

.. _add_user_to_group_example:
