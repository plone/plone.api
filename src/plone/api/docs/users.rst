User management
===============

Getting the API for a user
--------------------------

.. code-block:: python

   user = api.user(userobject)
   user = api.get_user(username)

.. invisible-code-block:: python

   None

Getting a user
--------------

.. code-block:: python
   # get user
   noob = api.users['noob']

.. invisible-code-block:: python
   None

Creating a user
---------------
a) api.users['newone'] = api.create_user(a, b, c)
b) api.users.create('someid', 'pass', a, b, c)

.. code-block:: python
   api.create_user('bob', firstname='Bob')

.. invisible-code-block:: python
   None

Deleting a user
---------------

.. code-block:: python
   del api.users['bob']

.. invisible-code-block:: python
   None


Changing a password
-------------------

.. code-block:: python
   user.password = 'foo$$'

.. invisible-code-block:: python
   None


Getting the currently logged in user
------------------------------------

.. code-block:: python
   api.get_current_user()

.. invisible-code-block:: python
   None


Getting the groups for a user
-----------------------------
.. code-block:: python
   api.user(userobj).get_groups()

.. invisible-code-block:: python
   ['group_a', 'group_b']


Adding a user to a group
------------------------

a) api.get_user('username').add_group('somegroup')
b) api.add_user_to_group('username', 'group')

.. code-block:: python
   # XXX this requires that get_user returns a API-wrapped user object
   api.get_user('username').add_group('somegroup')


Removing a group from a user
----------------------------

a) api.get_user('username').del_group('somegroup')
b) api.drop_group_from_user('someuser', 'somegroup')
c) del api.get_user('username').groups['somegroup']

.. code-block:: python
   None

.. invisible-code-block:: python
   None


Setting properties on a user
----------------------------

a) user['location'] = 'Munich'
b) user.setProperty(user, 'location', 'Munich')

.. code-block:: python
   user.setProperty(user, 'location', 'Munich')

.. invisible-code-block:: python
   None



