*******************************
:mod:`plone.api.user`
*******************************

:Author: Plone Foundation
:Version: |version|

.. module:: plone.api.user

.. topic:: Overview

   The :mod:`plone.api.user` provides CRUD methods for users and groups. 
   
User management
===============

Creating a user
---------------

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
   self.assertEquals(user.getProperty('email'), 'alice@plone.org')


Otherwise, you also need to pass in the username of the new user.

.. code-block:: python

   from plone import api
   user = api.user.create_user(email='jane@plone.org', username='jane')

.. invisible-code-block:: python

   self.assertEquals(user.id, 'jane')
   self.assertEquals(user.getProperty('email'), 'jane@plone.org')


To set user properties when creating a new user, pass in a properties dict.

.. code-block:: python

   properties = dict(
      fullname='Bob',
      location='Munich',
   )
   user = api.user.create_user(username='bob', email='bob@plone.org', properties=properties)

.. invisible-code-block:: python

   self.assertEquals(user.getProperty('fullname'), 'Bob')
   self.assertEquals(user.getProperty('location'), 'Munich')


Besides user properties you can also specify a password for the new user.
Otherwise a random 8-char alphanumeric password will be generated.

.. code-block:: python

   user = api.user.create_user(username='noob', email='noob@plone.org', password='secret')

.. invisible-code-block:: python

   self.assertEquals(user._getPassword(), 'secret')


Getting a user
--------------

.. code-block:: python

   from plone import api
   user = api.user.get(username='bob')

.. invisible-code-block:: python

   self.assertEquals(user.id, 'bob')


Getting the currently logged-in user
------------------------------------

.. code-block:: python

   from plone import api
   current = api.user.get_current()

.. invisible-code-block:: python

   self.assertEquals(current.id, 'test_user_1_')


Deleting a user
---------------

To delete a user, use ``delete`` and pass in either the username or the
user object you want to delete.

.. code-block:: python

   from plone import api
   unwanted = api.user.create(username='unwanted')
   api.user.delete('unwanted')


.. invisible-code-block:: python

   self.assertNone(api.user.get(username='unwanted'))

.. code-block:: python

   from plone import api
   unwanted = api.user.create(username='unwanted')
   api.user.delete(unwanted)


.. invisible-code-block:: python

   self.assertNone(api.user.get(username='unwanted'))


Changing a password
-------------------

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


Getting a user's property
-------------------------

Use ``get_property`` and pass in either the username or the user object you want
to get property for, plus the name of the property.

.. code-block:: python

    email = api.user.get_property(username='bob', name='email')

.. invisible-code-block:: python

    self.assertEqulas(email, 'bob@plone.org')


Setting a user's property
-------------------------

Setting a user's property is achieved by using ``set_property``, passing it
either the username or the user object you want to get property for,
plus the name of the property and it's new value.

.. code-block:: python

    api.user.set_property(username='bob', name='email', value='bob@plone.com')

.. invisible-code-block:: python

    email = api.user.get_property(username='bob', name='email')
    self.assertEqulas(email, 'bob@plone.com')


Getting groups that user is a member of
---------------------------------------

Use ``get_groups``, passing in either the username or the user object you want
to get groups for.

.. code-block:: python

   groups = api.user.get_groups(username='bob')

.. invisible-code-block:: python

   self.assertEquals(groups, ['staff', ])


Adding a user to a group
------------------------

The ``join_group`` method accepts either the username or the user object you want
to make a member of the group and either the groupname or the group object of
the target group.

.. code-block:: python

   api.user.join_group(username='bob', groupname='staff')

   user = api.user.get(username='jane')
   group = api.group.get(groupname='staff')
   api.user.join_group(user=user, group=group)

.. code-block:: python

   self.assertEquals(api.user.get_groups(username='bob'), ['staff, '])
   self.assertEquals(api.user.get_groups(username='jane'), ['staff, '])


Remove user from a group
------------------------

The ``leave_group`` method accepts either the username or the user object you
want to remove from the group and either the groupname or the group object of
the target group.

.. code-block:: python

   api.user.leave_group(username='bob', groupname='staff')

   user = api.user.get(username='jane')
   group = api.group.get(groupname='staff')
   api.user.leave_group(user=user, group=group)

.. invisible-code-block:: python

   self.assertEquals(api.user.get_groups(username='bob'), [])
   self.assertEquals(api.user.get_groups(username='jane'), [])

