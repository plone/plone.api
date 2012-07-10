Managing content
================

.. _create_content_example:

Create content
--------------

First get the site object thru the api:

.. code-block:: python

    from plone import api
    site = api.get_site()

If you want to create a new content item, use this method. The type attribute
will automatically decide which content type (dexterity, archetype, ...) should
be created.

.. code-block:: python

    from plone.api import content
    obj = content.create(type='Document', title='My Content', container=site)

.. invisible-code-block:: python

    self.assertEquals(obj.Title(), 'My Content')

The object's ``id`` gets generated (in a safe way) from it's ``title``.

.. code-block:: python

    self.assertEquals(obj.id, 'my-content')

.. invisible-code-block:: python

    self.assertEquals(obj.Title(), 'My Content')


If you want to make sure that the ``id`` will be the one you'd expect from your
``title`` or ``id`` parameter, just pass the ``strict=True`` parameter and
``create`` will raise a ``KeyError`` if ``id`` conflicts.

.. invisible-code-block:: python

    obj = None

.. code-block:: python

    try:
        content.create(
            type='Document', title='My Content', id='my-content', container=site, strict=True
        )
    except KeyError:
        pass

.. invisible-code-block:: python

    self.assertFalse(obj)


.. _get_content_example:

Get content object
------------------

There are several approaches of getting to your content object. Consider
the following site structure::

    Plone (site root)
    |-- welcome
    |-- about
    |   |-- team
    |   `-- contact
    `-- events
        |-- training
        |-- conference
        `-- sprint

.. invisible-code-block:: python

    site = api.get_site()
    welcome = api.content.create(type='Document', id='welcome', container=site)
    about = api.content.create(type='Folder', id='about', container=site)
    events = api.content.create(type='Folder', id='events', container=site)

    api.content.create(container=about, type='Document', id='team')
    api.content.create(container=about, type='Document', id='contact')

    api.content.create(container=events, type='Event', id='training')
    api.content.create(container=events, type='Event', id='conference')
    api.content.create(container=events, type='Event', id='sprint')


We can do the following operations to get to various content objects in the
stucture above:

.. code-block:: python

    from plone import api
    site = api.get_site()             # the root object
    self.assertEqual(site.getId(), 'plone')

    site = api.content.get(path='/')  # this also works
    self.assertEqual(site.getId(), 'plone')

    welcome = site['welcome']  # your can access children directly with dict-like access
    welcome_by_path = api.content.get(path='/welcome')  # or indirectly by using the api.content.get() method

    self.assertEqual(welcome, welcome_by_path)
    # more examples
    conference = site['events']['conference']
    sprint = api.content.get(path='/events/training')

    # Check resolving by UID
    uid = conference.UID()
    conference_by_uid = api.content.get(UID=uid)

    self.assertEqual(conference, conference_by_uid)


.. _move_content_example:

Move content
------------

This is how you can move content around the site structure defined above.
The code below moves item ``contact`` (with all objects that it contains) ouf
of folder ``about`` into Plone site root.

.. code-block:: python

    from plone import api
    site = api.get_site()
    contact = site['about']['contact']

    api.content.move(source=contact, target=site)

.. invisible-code-block:: python

    self.assertTrue(site['contact'])

Actually, ``move`` behaves like a filesystem move. If you pass it an ``id``
argument, you can define to what target ID the object will be moved to.
Otherwise it will be moved with the same ID that it had.

If the ID in the target folder is already used, a new non-conflicting ID is
being generated. If you don't like that, just add another argument
``strict=True`` to make move raise a ``KeyError`` if the target ID exists.

.. code-block:: python

    from plone import api
    site = api.get_site()
    contact = site['contact']

    from OFS.CopySupport import CopyError
    self.assertRaises(
        CopyError,
        api.content.move,
        source=contact, target=site, id='contact', strict=True
    )

.. _rename_content_example:

Rename content
--------------

To rename, you still use the ``move`` method, just pass in a new ``id`` instead
and omit ``target``.

.. code-block:: python

    from plone import api
    site = api.get_site()
    api.content.move(source=site['welcome'], id='very-welcome')

.. invisible-code-block:: python

    self.assertTrue(site['very-welcome'])

Again, you may use the argument ``strict=True`` to make move raise a
``KeyError`` if the target ID was already used.

.. code-block:: python

    from plone import api
    site = api.get_site()
    try:
        api.content.move(source=site['very-welcome'], id='very-welcome')
    except KeyError:
        pass  # do something meaningful, because the ID was already owned.


.. _copy_content_example:

Copy content
------------

To copy a content object, use this:

.. code-block:: python

    from plone import api
    site = api.get_site()
    training = site['events']['training']

    api.content.copy(source=training, target=site)


Note that the new object will have the same id as the old object (if not
stated otherwise).

.. code-block:: python

    self.assertTrue(site['training'])


However, if the new object's id conflicts with another object in the target
container, a suffix will be added to the new object's id.

.. code-block:: python

    api.content.copy(source=training, target=site)  # copy again
    self.assertTrue(site['training-1'])


You can also just omit ``target`` which will duplicate your content object
in the same container where it already is and assign it a non-conflicting id.

.. code-block:: python

    api.content.copy(source=training)
    self.assertTrue(site['events']['training-1'])

With the parameter ``strict=True``, copy will raise a ``KeyError`` if the
target ID conflicts with an existing one in the target folder.

.. code-block:: python

    try:
        api.content.copy(source=training, target=site, id='training', strict=True) # copy again
    except KeyError:
        pass # do something meaningful, because the ID was already owned.

.. invisible-code-block:: python

    self.assertTrue(site['training'])


.. _delete_content_example:

Delete content
--------------

Deleting content works like this:

.. code-block:: python

    from plone import api
    site = api.get_site()
    redundant_training = site['training-1']
    api.content.delete(obj=redundant_training)

.. invisible-code-block:: python

    self.assertNotIn('training-1', site)


.. _get_state_example:

Get workflow state
------------------

To find out in which workflow state your content is, use ``get_state``.

.. code-block:: python

    from plone import api
    about = site['about']
    state = api.content.get_state(about)

.. invisible-code-block:: python

    self.assertEquals(state, 'private')


.. _transition_example:

Transition
----------

To transition your content into a new state, use ``transition``.

.. code-block:: python

    from plone import api
    about = site['about']
    state = api.content.transition(obj=about, transition='publish')

.. invisible-code-block:: python

    self.assertEquals(state, 'published')

