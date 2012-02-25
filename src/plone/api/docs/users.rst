User management
===============

Creating a user
---------------

To create a new user, use this.


.. code-block:: python

   from plone import api
   api.create_user('bob', firstname='Bob')

.. invisible-code-block:: python

   None

You can also add groups to that user:

.. code-block:: python

   from plone import api
   api.create_user('eliza', groups=['group_a', 'group_b'])

.. invisible-code-block:: python

   None


Getting a user
--------------

.. code-block:: python

   from plone import api
   api.create_user('noob', firstname='Noob Ie')
   noob = api.get_user('noob')

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


