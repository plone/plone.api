Managing users
==============

.. _create_user_example:

Create user
-----------

If your site is configured to use emails as usernames you just need to pass
in the email of the new user.

.. invisible-code-block:: python

    from plone import api
    site = api.get_site()
    site.portal_properties.use_email_as_username = True

.. code-block:: python

    from plone import api
    user = api.user.create_user(email='alice@plone.org')

.. invisible-code-block:: python

    self.assertEquals(user.id, 'alice@plone.org')
    self.assertEquals(api.user.get_property(user=user, name='email'), 'alice@plone.org')


Otherwise, you also need to pass in the username of the new user.

.. code-block:: python

    user = api.user.create_user(email='jane@plone.org', username='jane')

.. invisible-code-block:: python

    self.assertEquals(user.id, 'jane')
    self.assertEquals(api.user.get_property(user=user, name='email'), 'jane@plone.org')


To set user properties when creating a new user, pass in a properties dict.

.. code-block:: python

    properties = dict(
        fullname='Bob',
        location='Munich',
    )
    user = api.user.create_user(username='bob', email='bob@plone.org', properties=properties)

.. invisible-code-block:: python

    self.assertEquals(api.user.get_property(user=user, name='fullname'), 'Bob')
    self.assertEquals(api.user.get_property(user=user, name='location'), 'Munich')


Besides user properties you can also specify a password for the new user.
Otherwise a random 8-char alphanumeric password will be generated.

.. code-block:: python

    user = api.user.create_user(username='noob', email='noob@plone.org', password='secret')

.. invisible-code-block:: python

    self.assertEquals(user._getPassword(), 'secret')


.. _get_user_example:

Get user
--------

.. code-block:: python

    from plone import api
    user = api.user.get(username='bob')

.. invisible-code-block:: python

    self.assertEquals(user.id, 'bob')


.. _get_current_user_example:

Get currently logged-in user
----------------------------

.. code-block:: python

    from plone import api
    current = api.user.get_current()

.. invisible-code-block:: python

    self.assertEquals(current.id, 'test_user_1_')


.. _is_anonymous_example:

Check if current user is anonymous
----------------------------------

Sometimes you need to trigger or display some piece of information only for
logged-in users. It's easy to use ``is_anonymous`` to do a basic check for it.

.. code-block:: python

    from plone import api
    if not api.user.is_anonymous():
        trigger = False
    trigger = True

.. invisible-code-block:: python

    self.assertTrue(trigger)


.. _get_all_users_example:

Get all users
-------------

.. code-block:: python

    from plone import api
    users = api.user.get_all()

.. invisible-code-block:: python

    self.assertEquals(users[0].id, 'test_user_1_')


.. _delete_user_example:

Delete user
-----------

To delete a user, use ``delete`` and pass in either the username or the
user object you want to delete.

.. code-block:: python

    from plone import api
    api.user.create(username='unwanted')
    api.user.delete(username='unwanted')


.. invisible-code-block:: python

    self.assertNone(api.user.get(username='unwanted'))

.. code-block:: python

    unwanted = api.user.create(username='unwanted')
    api.user.delete(user=unwanted)

.. invisible-code-block:: python

    self.assertNone(api.user.get(username='unwanted'))


.. _change_password_example:

Change user's password
----------------------

To change a user's password, use ``change_password`` and pass in either the
username or the user object you want to change password for, plus the password
you want the new user to have.

If you don't pass in any password, a random one will be generated.

.. code-block:: python

    from plone import api
    api.user.change_password(username='bob', password='newsecret')

.. invisible-code-block:: python

    self.assertEqulas(user._getPassword(), password='newsecret')

.. code-block:: python

    api.user.change_password(user=user, password='newsecret')

.. invisible-code-block:: python

    self.assertEqulas(user._getPassword(), password='newnewsecret')

.. code-block:: python

    api.user.change_password(username='bob')  # generate a random password


.. _get_user_property_example:

Get user's property
-------------------

Use ``get_property`` and pass in either the username or the user object you want
to get property for, plus the name of the property.

.. code-block:: python

    from plone import api
    email = api.user.get_property(username='bob', name='email')

.. invisible-code-block:: python

    self.assertEquals(email, 'bob@plone.org')


.. _set_user_property_example:

Set user's property
-------------------

Setting a user's property is achieved by using ``set_property``, passing it
either the username or the user object you want to get property for,
plus the name of the property and it's new value.

.. code-block:: python

    from plone import api
    api.user.set_property(username='bob', name='email', value='bob@plone.com')

.. invisible-code-block:: python

    self.assertEquals(bob.getProperty('email'), 'Bob Smith', 'bob@plone.com')


.. _has_role_example:

Check for role
--------------

Again on the security aspects, checking if a user has a certain role goes
like this. If you omit the ``user`` parameter, the currently logged-in
user will be used.

.. code-block:: python

    from plone import api
    if not api.user.has_role(username='bob', role='Manager'):
        trigger = False
    trigger = True

.. invisible-code-block:: python

    self.assertFalse(trigger)


.. _has_permission_example:

Check for permission
--------------------

Likewise, you can also check if a user has a certain permission. Omitting the
``user`` parameter means the currently logged-in user will be used.

.. code-block:: python

    from plone import api
    if not api.user.has_permission(username='bob', permission='Manage portal content'):
        trigger = False
    trigger = True

.. invisible-code-block:: python

    self.assertFalse(trigger)


.. _get_groups_for_user_example:

Get groups that user is a member of
-----------------------------------

Use ``get_groups``, passing in either the username or the user object you want
to get groups for.

.. code-block:: python

    from plone import api
    groups = api.user.get_groups(username='bob')

.. invisible-code-block:: python

    self.assertEquals(groups, ['staff', ])


.. _add_user_to_group_example:

Add user to group
-----------------

The ``join_group`` method accepts either the username or the user object you
want to make a member of the group and either the groupname or the group object
of the target group.

.. code-block:: python

    from plone import api
    api.user.join_group(username='bob', groupname='staff')

    user = api.user.get(username='jane')
    group = api.group.get(groupname='staff')
    api.user.join_group(user=user, group=group)

.. invisible-code-block:: python

    self.assertEquals(api.user.get_groups(username='bob'), ['staff, '])
    self.assertEquals(api.user.get_groups(username='jane'), ['staff, '])


.. _remove_user_from_group_example:

Remove user from group
----------------------

The ``leave_group`` method accepts either the username or the user object you
want to remove from the group and either the groupname or the group object of
the target group.

.. code-block:: python

    from plone import api
    api.user.leave_group(username='bob', groupname='staff')

    user = api.user.get(username='jane')
    group = api.group.get(groupname='staff')
    api.user.leave_group(user=user, group=group)

.. invisible-code-block:: python

    self.assertEquals(api.user.get_groups(username='bob'), [])
    self.assertEquals(api.user.get_groups(username='jane'), [])
