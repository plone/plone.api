User management
===============

Getting the API for a user
--------------------------

.. testcode::

   user = api.user(userobject)
   user = api.get_user(username)

.. testoutput::

   None

Getting a user
--------------

.. testcode::
   # get user
   noob = api.users['noob']

.. testoutput::
   None

Creating a user
---------------
a) api.users['newone'] = api.create_user(a, b, c)
b) api.users.create('someid', 'pass', a, b, c)

.. testcode::
   api.create_user('bob', firstname='Bob')

.. testoutput::
   None

Deleting a user
---------------

.. testcode::
   del api.users['bob']

.. testoutput::
   None


Changing a password
-------------------

.. testcode::
   user.password = 'foo$$'

.. testoutput::
   None


Getting the currently logged in user
------------------------------------

.. testcode::
   api.get_current_user()

.. testoutput::
   None


Getting the groups for a user
-----------------------------
.. testcode::
   api.user(userobj).get_groups()

.. testoutput::
   ['group_a', 'group_b']


Adding a user to a group
------------------------

a) api.get_user('username').add_group('somegroup')
b) api.add_user_to_group('username', 'group')

.. testcode::
   # XXX this requires that get_user returns a API-wrapped user object
   api.get_user('username').add_group('somegroup')


Removing a group from a user
----------------------------

a) api.get_user('username').del_group('somegroup')
b) api.drop_group_from_user('someuser', 'somegroup')
c) del api.get_user('username').groups['somegroup']

.. testcode::
   None

.. testoutput::
   None


Setting properties on a user
----------------------------

a) user['location'] = 'Munich'
b) user.setProperty(user, 'location', 'Munich')

.. testcode::
   user.setProperty(user, 'location', 'Munich')

.. testoutput::
   None



