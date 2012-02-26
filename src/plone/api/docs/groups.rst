Managing groups
===============

.. _create_group_example:

Creating a group
----------------

.. code-block:: python

    from plone import api
    group = api.group.create_group(groupname='staff')

.. invisible-code-block:: python

    self.assertEquals(group.id, 'staff')


.. _get_group_example:

Getting a group
---------------

.. code-block:: python

    from plone import api
    group = api.group.get(groupname='staff')

.. invisible-code-block:: python

    self.assertEquals(group.id, 'staff')


.. _get_all_groups_example:

Getting all groups
------------------

.. code-block:: python

    from plone import api
    users = api.group.get_all()

.. invisible-code-block:: python

    self.assertEquals(group[0].id, 'staff')


.. _delete_group_example:

Deleting a group
----------------

To delete a group, use ``delete`` and pass in either the groupname or the
group object you want to delete.

.. code-block:: python

    from plone import api
    api.group.create(groupname='unwanted')
    api.group.delete(groupname='unwanted')

.. invisible-code-block:: python

    self.assertNone(api.group.get(groupname='unwanted'))

.. code-block:: python

    unwanted = api.group.create(groupname='unwanted')
    api.group.delete(group=unwanted)

.. invisible-code-block:: python

    self.assertNone(api.group.get(groupname='unwanted'))
