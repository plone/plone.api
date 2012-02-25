User management
===============

Creating a user
---------------

To quickly create a new user, use the ``create_user`` helper method. You have
to specify username id and email.

.. code-block:: python

   from plone import api
   user = api.create_user(username='alice', email='alice@plone.org')

.. invisible-code-block:: python

   self.assertEquals(user.id, 'alice')
   self.assertEquals(user.getProperty('email'), 'alice@plone.org')

You can specify any number of user properties as keyword arguments.

.. code-block:: python

   user = api.create_user('bob', email='bob@plone.org',
      fullname='Bob',
      location='Munich',
   )

.. invisible-code-block:: python

   self.assertEquals(user.getProperty('fullname'), 'Bob')
   self.assertEquals(user.getProperty('location'), 'Munich')

Besides user properties you can also specify a password for the new user.
Otherwise a random 8-char alphanumeric password will be generated.

.. code-block:: python

   user = api.create_user('noob', email='noob@plone.org', password='secret')

.. invisible-code-block:: python

   # TODO: self.assertEquals(user.getPassword(), 'secret')


Getting a user
--------------

.. code-block:: python

   from plone.api import users
   bob = users['bob']

.. invisible-code-block:: python

   # TODO Add test!
   None

Deleting a user
---------------

.. code-block:: python

   from plone import api
   api.create_user('unwanted')
   api.del_user['unwanted']

.. invisible-code-block:: python

   self.assertNone(api.get_user('unwanted'))


Changing a password
-------------------

.. code-block:: python

   from plone import api
   api.create_user('forgotpw')
   api.change_password('forgotpw', 'qwerty')

.. invisible-code-block:: python

   # TODO Add test!
   None

.. invisible-code-block:: python

   user._getPassword('new-password')


Getting the currently logged in user
------------------------------------

.. code-block:: python

   user = api.get_current_user()

.. invisible-code-block:: python

   # TODO Write better test
   self.assertNotNone(user)


Getting the groups for a user
-----------------------------

.. code-block:: python

   api.create_user('getmygroups', groups=['group_a', 'group_b'])
   groups = api.get_groups('getmygroups')

.. invisible-code-block:: python

   self.assertEquals(groups, ['group_a', 'group_b'])


Adding a user to a group
------------------------

.. code-block:: python

   api.create_user('groupie')
   api.add_user_to_group('groupie', 'group_c')

.. code-block:: python

   groups = api.get_groups('groupie')
   self.assertEquals(groups, ['group_c'])


Removing a group from a user
----------------------------

.. code-block:: python

   api.create_user('removemygroups', groups=['group_d', 'group_e'])
   api.drop_group_from_user('removemygroups', 'group_d')

.. invisible-code-block:: python

   groups = api.get_groups('removemygroups')
   self.assertEquals(groups, ['group_e'])


User properties
---------------

Setting a property

.. code-block:: python

   api.create_user('propie')
   api.set_user_property('propie', 'location', 'Munich')

.. invisible-code-block:: python

   self.assertEquals(api.get_user_property('propie', 'location'), 'Munich')


...and getting a property

.. code-block:: python

   location = api.get_user_property('propie', 'location')


