Managing content
================

.. _create_content_example:

Create content
--------------

First get the portal object that we will use as a container for new content:

.. code-block:: python

    from plone import api
    portal = api.portal.get()

If you want to create a new content item, use the ``create`` method. The type
attribute will automatically decide which content type (dexterity, archetype,
...) should be created.

.. code-block:: python

    from plone.api import content
    obj = content.create(
        type='Document',
        title='My Content',
        container=portal
    )

The object's ``id`` gets generated (in a safe way) from it's ``title``.

.. code-block:: python

    assert obj.id == 'my-content'


.. _get_content_example:

Get content object
------------------

There are several approaches of getting to your content object. Consider
the following portal structure::

    plone (portal root)
    |-- blog
    |-- about
    |   |-- team
    |   `-- contact
    `-- events
        |-- training
        |-- conference
        `-- sprint

.. invisible-code-block:: python

    portal = api.portal.get()
    blog = api.content.create(type='Link', id='blog', container=portal)
    about = api.content.create(type='Folder', id='about', container=portal)
    events = api.content.create(type='Folder', id='events', container=portal)

    api.content.create(container=about, type='Document', id='team')
    api.content.create(container=about, type='Document', id='contact')

    api.content.create(container=events, type='Event', id='training')
    api.content.create(container=events, type='Event', id='conference')
    api.content.create(container=events, type='Event', id='sprint')


You can do the following operations to get to various content objects in the
stucture above:

.. code-block:: python

    # let's first get the portal object
    from plone import api
    portal = api.portal.get()
    assert portal.id == 'plone'

    # content can be accessed directly with dict-like access
    blog = portal['blog']

    # another way is to use ``get()`` method and pass it a path
    about = api.content.get(path='/about')

    # more examples
    conference = portal['events']['conference']
    sprint = api.content.get(path='/events/sprint')

    # moreover, you can access content by it's UID
    uid = about['team'].UID()
    conference = api.content.get(UID=uid)


.. invisible-code-block:: python

    self.assertTrue(portal)
    self.assertTrue(blog)
    self.assertTrue(about)
    self.assertTrue(conference)
    self.assertTrue(sprint)


.. _move_content_example:

Move content
------------

This is how you can move content around the portal structure defined above.
The code below moves the ``contact`` item (with all objects that it contains)
out of folder ``about`` into the Plone portal root.

.. code-block:: python

    from plone import api
    portal = api.portal.get()
    contact = portal['about']['contact']

    api.content.move(source=contact, target=portal)

.. invisible-code-block:: python

    self.assertFalse(portal['about'].get('contact'))
    self.assertTrue(portal['contact'])

Actually, ``move`` behaves like a filesystem move. If you pass it an ``id``
argument, you can define to what target ID the object will be moved to.
Otherwise it will be moved with the same ID that it had.


.. _rename_content_example:

Rename content
--------------

To rename, you still use the ``move`` method, just pass in a new ``id`` instead
and omit ``target``.

.. code-block:: python

    from plone import api
    portal = api.portal.get()
    api.content.move(source=portal['blog'], id='old-blog')

.. invisible-code-block:: python

    self.assertFalse(portal.get('blog'))
    self.assertTrue(portal['old-blog'])


.. _copy_content_example:

Copy content
------------

To copy a content object, use the following:

.. code-block:: python

    from plone import api
    portal = api.portal.get()
    training = portal['events']['training']

    api.content.copy(source=training, target=portal)


Note that the new object will have the same id as the old object (if not
stated otherwise). This is not a problem, since the new object is in a different
container.

.. code-block:: python

    assert portal['events']['training'].id == 'training'
    assert portal.id == 'training'


You can also omit ``target`` and set ``strict=False`` which will duplicate your
content object in the same container and assign it a non-conflicting id.

.. code-block:: python

    api.content.copy(source=training, strict=False)
    new_training = portal['events']['training-1']

.. invisible-code-block:: python

    self.assertTrue(portal['events']['training'])  # old object remains
    self.assertTrue(portal['events']['training-1'])


.. _delete_content_example:

Delete content
--------------

Deleting content works by passing the object you want to delete to the
``delete()`` method:

.. code-block:: python

    from plone import api
    portal = api.portal.get()
    api.content.delete(obj=portal['training-1'])

.. invisible-code-block:: python

    self.assertFalse(portal.get('training-1'))


.. _content_manipulation_with_strict_option

Content manipulation with strict option
---------------------------------------

When manipulating content with ``api.content.create``, ``api.content.move`` and ``api.content.copy``
the strict option is enabled by default. This means the id will be enforced, if the id is taken on
the target container the API method will raise an error.

.. code-block:: python

    api.content.create(container=portal, type='Document', id='non-strict-usage')
    portal['non-strict-usage']

If the strict option is disabled a non-conflicting id will be created.

.. code-block:: python
    api.content.create(container=portal, type='Document', id='non-strict-usage', strict=False)
    portal['non-strict-usage-1']


.. _get_state_state:

Get workflow state
------------------

To find out in which workflow state your content is, use ``get_state``.

.. code-block:: python

    from plone import api
    portal = api.portal.get()
    state = api.content.get_state(obj=portal['about'])

.. invisible-code-block:: python

    self.assertEquals(state, 'private')


.. _transition_example:

Transition
----------

To transition your content into a new state, use ``transition``.

.. code-block:: python

    from plone import api
    portal = api.portal.get()
    state = api.content.transition(obj=portal['about'], transition='publish')

.. invisible-code-block:: python

    self.assertEquals(state, 'published')


Further reading
---------------

For more information on possible flags and usage options please see the full
:ref:`plone-api-content` specification.
