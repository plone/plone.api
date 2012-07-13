.. module:: plone

.. _chapter_content:

Content
=======

.. _content_create_example:

Create content
--------------

First get the portal object that we will use as a container for new content:

.. code-block:: python

    from plone import api
    portal = api.portal.get()

If you want to create a new content item, use the :meth:`api.content.create`
method. The type attribute will automatically decide which content type
(dexterity, archetype, ...) should be created.

.. code-block:: python

    from plone import api
    obj = api.content.create(
        type='Document',
        title='My Content',
        container=portal)

The ``id`` of the object gets generated (in a safe way) from its ``title``.

.. code-block:: python

    assert obj.id == 'my-content'


.. _content_get_example:

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
stucture above, including using :meth:`api.content.get`.

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


.. _content_find_example:

Find content object
-------------------

You can use the *catalog* to search for content. Here is a simple example:

.. code-block:: python

    from plone import api
    catalog = api.portal.get_tool(name='portal_catalog')
    documents = catalog(portal_type='Document')

.. invisible-code-block:: python
    self.assertEqual(catalog.__class__.__name__, 'CatalogTool')
    self.assertEqual(len(documents), 3)

More about how to use the catalog and what parameters it supports is written
in the `Collective Developer Documentation
<http://collective-docs.readthedocs.org/en/latest/searching_and_indexing/query.html>`_.
Note that the catalog returns *brains* (metadata stored in indexes) and not
objects. However, calling ``getObject()`` on brains does in fact give you the
object.

.. code-block:: python

    document_brain = documents[0]
    document_obj = document_brain.getObject()
    assert document_obj.__class__.__name__ == 'ATDocument'

.. _content_move_example:

Move content
------------

To move content around the portal structure defined above use
:meth:`api.content.move` The code below moves the ``contact`` item (with all
objects that it contains) out of folder ``about`` into the Plone portal root.

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


.. _content_rename_example:

Rename content
--------------

To rename, you still use the :meth:`api.content.move` method, just pass in a
new ``id`` instead and omit ``target``.

.. code-block:: python

    from plone import api
    portal = api.portal.get()
    api.content.move(source=portal['blog'], id='old-blog')

.. invisible-code-block:: python

    self.assertFalse(portal.get('blog'))
    self.assertTrue(portal['old-blog'])


.. _content_copy_example:

Copy content
------------

To copy a content object, use the :meth:`api.content.copy`.

.. code-block:: python

    from plone import api
    portal = api.portal.get()
    training = portal['events']['training']

    api.content.copy(source=training, target=portal)

Note that the new object will have the same id as the old object (if not
stated otherwise). This is not a problem, since the new object is in a different
container.

.. invisible-code-block:: python

    assert portal['events']['training'].id == 'training'
    assert portal['training'].id == 'training'


You can also omit ``target`` and set ``strict=False`` which will duplicate your
content object in the same container and assign it a non-conflicting id.

.. code-block:: python

    api.content.copy(source=training, target=portal['events'], strict=False)
    new_training = portal['events']['copy_of_training']

.. invisible-code-block:: python

    self.assertTrue(portal['events']['training'])  # old object remains
    self.assertTrue(portal['events']['copy_of_training'])


.. _content_delete_example:

Delete content
--------------

Deleting content works by passing the object you want to delete to the
:meth:`api.content.delete` method:

.. code-block:: python

    from plone import api
    portal = api.portal.get()
    api.content.delete(obj=portal['events']['copy_of_training'])

.. invisible-code-block:: python

    self.assertFalse(portal['events'].get('copy_of_training'))


.. _content_manipulation_with_strict_option:

Content manipulation with strict option
---------------------------------------

When manipulating content with :meth:`api.content.create`,
:meth:`api.content.move` and :meth:`api.content.copy` the strict option is
enabled by default. This means the id will be enforced, if the id is taken on
the target container the API method will raise an error.

.. code-block:: python

    api.content.create(container=portal, type='Document', id='non-strict-usage')
    portal['non-strict-usage']

If the strict option is disabled a non-conflicting id will be created.

.. code-block:: python
    api.content.create(container=portal, type='Document', id='non-strict-usage', strict=False)
    portal['non-strict-usage-1']


.. _content_get_state_example:

Get workflow state
------------------

To find out in which workflow state your content is, use
:meth:`api.content.get_state`.

.. code-block:: python

    from plone import api
    portal = api.portal.get()
    state = api.content.get_state(obj=portal['about'])

.. invisible-code-block:: python

    self.assertEquals(state, 'private')


.. _content_transition_example:

Transition
----------

To transition your content into a new state, use :meth:`api.content.transition`.

.. code-block:: python

    from plone import api
    portal = api.portal.get()
    state = api.content.transition(obj=portal['about'], transition='publish')

.. invisible-code-block:: python

    self.assertEquals(
        api.content.get_state(obj=portal['about']),
        'published'
    )


.. _conten_get_view_example:

Browser view
------------

To get a BrowserView for your content, use :meth:`api.content.get_view`.

.. code-block:: python

    from plone import api
    portal = api.portal.get()
    view = api.content.get_view(
        name='plone',
        context=portal['about'],
        request=request,
    )

.. invisible-code-block:: python

    self.assertEquals(view.__name__, u'plone')


Further reading
---------------

For more information on possible flags and usage options please see the full
:ref:`plone-api-content` specification.
