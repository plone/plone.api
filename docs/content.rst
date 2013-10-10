.. admonition:: GitHub-only

    WARNING: If you are reading this on GitHub, DON'T! Read the documentation
    at `api.plone.org <http://developer.plone.org/reference_manuals/external/plone.api/content.html>`_
    so you have working references and proper formatting.


.. module:: plone

.. _chapter_content:

Content
=======

.. _content_create_example:

Create content
--------------

To add an object, you must first have a container in which to put it. Get the
portal object, it will serve nicely:

.. code-block:: python

    from plone import api
    portal = api.portal.get()

Create your new content item using the :meth:`api.content.create` method. The
type argument will decide which content type will be created. Both Dexterity
and Archetypes content types are supported.

.. code-block:: python

    from plone import api
    obj = api.content.create(
        type='Document',
        title='My Content',
        container=portal)

The ``id`` of the new object is automatically and safely generated from its
``title``.

.. code-block:: python

    assert obj.id == 'my-content'


.. _content_get_example:

Get content object
------------------

There are several approaches to getting your content object. Consider the
following portal structure::

    plone (portal root)
    |-- blog
    |-- about
    |   |-- team
    |   `-- contact
    `-- events
        |-- training
        |-- conference
        `-- sprint

.. invisible-code-block: python

    portal = api.portal.get()
    blog = api.content.create(type='Link', id='blog', container=portal)
    about = api.content.create(type='Folder', id='about', container=portal)
    events = api.content.create(type='Folder', id='events', container=portal)

    api.content.create(container=about, type='Document', id='team')
    api.content.create(container=about, type='Document', id='contact')

    api.content.create(container=events, type='Event', id='training')
    api.content.create(container=events, type='Event', id='conference')
    api.content.create(container=events, type='Event', id='sprint')


The following operations will get objects from the stucture above, including
using :meth:`api.content.get`.

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

    # moreover, you can access content by its UID
    uid = about['team'].UID()
    team = api.content.get(UID=uid)


.. invisible-code-block: python

    self.assertTrue(portal)
    self.assertTrue(blog)
    self.assertTrue(about)
    self.assertTrue(conference)
    self.assertTrue(sprint)
    self.assertTrue(team)


.. _content_find_example:

Find content objects
--------------------

You can use the *catalog* to search for content. Here is a simple example:

.. code-block:: python

    from plone import api
    catalog = api.portal.get_tool(name='portal_catalog')
    documents = catalog(portal_type='Document')

.. invisible-code-block: python
    self.assertEqual(catalog.__class__.__name__, 'CatalogTool')
    self.assertEqual(len(documents), 3)

More information about how to use the catalog may be found in the `Collective
Developer Documentation
<http://collective-docs.readthedocs.org/en/latest/searching_and_indexing/query.html>`_.
Note that the catalog returns *brains* (metadata stored in indexes) and not
objects. However, calling ``getObject()`` on brains does in fact give you the
object.

.. code-block:: python

    document_brain = documents[0]
    document_obj = document_brain.getObject()
    assert document_obj.__class__.__name__ == 'ATDocument'

.. _content_get_uuid_example:

Get content object UUID
-----------------------

A Universally Unique IDentifier (UUID) is a unique, non-human-readable
identifier for a content object which stays on the object even if the object
is moved.

Plone uses UUIDs for storing references between content and for linking by
UIDs, enabling persistent links.

To get the UUID of any content object use :meth:`api.content.get_uuid`. The
following code gets the UUID of the ``contact`` document.

.. code-block:: python

    from plone import api
    portal = api.portal.get()
    contact = portal['about']['contact']

    uuid = api.content.get_uuid(obj=contact)

.. invisible-code-block: python

    self.assertTrue(isinstance(uuid, str))

.. _content_move_example:

Move content
------------

To move content around the portal structure defined above use the
:meth:`api.content.move` method. The code below moves the ``contact`` item
(with all it contains) out of the folder ``about`` and into the Plone portal
root.

.. code-block:: python

    from plone import api
    portal = api.portal.get()
    contact = portal['about']['contact']

    api.content.move(source=contact, target=portal)

.. invisible-code-block: python

    self.assertFalse(portal['about'].get('contact'))
    self.assertTrue(portal['contact'])

Actually, ``move`` behaves like a filesystem move. If you pass it an ``id``
argument the object will have that new ID in it's new home. By default it will
retain its original ID.

.. _content_rename_example:

Rename content
--------------

To rename a content object (change its ID), use the :meth:`api.content.rename`
method.

.. code-block:: python

    from plone import api
    portal = api.portal.get()
    api.content.rename(obj=portal['blog'], new_id='old-blog')

.. invisible-code-block: python

    self.assertFalse(portal.get('blog'))
    self.assertTrue(portal['old-blog'])


.. _content_copy_example:

Copy content
------------

To copy a content object, use the :meth:`api.content.copy` method.

.. code-block:: python

    from plone import api
    portal = api.portal.get()
    training = portal['events']['training']

    api.content.copy(source=training, target=portal)

Note that the new object will have the same ID as the old object (unless
otherwise stated). This is not a problem, since the new object is in a
different container.

.. invisible-code-block: python

    assert portal['events']['training'].id == 'training'
    assert portal['training'].id == 'training'


You can also set ``target`` to source's container and set ``safe_id=True`` which
will duplicate your content object in the same container and assign it a
new, non-conflicting ID.

.. code-block:: python

    api.content.copy(source=portal['training'], target=portal, safe_id=True)
    new_training = portal['copy_of_training']

.. invisible-code-block: python

    self.assertTrue(portal['training'])  # old object remains
    self.assertTrue(portal['copy_of_training'])


.. _content_delete_example:

Delete content
--------------

To delete a content object, pass the object to the :meth:`api.content.delete`
method:

.. code-block:: python

    from plone import api
    portal = api.portal.get()
    api.content.delete(obj=portal['copy_of_training'])

.. invisible-code-block: python

    self.assertFalse(portal.get('copy_of_training'))


.. _content_manipulation_with_safe_id_option:

Content manipulation with the `safe_id` option
----------------------------------------------

When manipulating content with :meth:`api.content.create`,
:meth:`api.content.move` or :meth:`api.content.copy` the `safe_id` flag is
disabled by default. This means the uniqueness of IDs will be enforced. If
another object with the same ID is already present in the target container
these API methods will raise an error.

However, if the `safe_id` option is enabled, a non-conflicting id will be
generated.

.. invisible-code-block: python

    api.content.create(container=portal, type='Document', id='document', safe_id=True)

.. code-block:: python

    api.content.create(container=portal, type='Document', id='document', safe_id=True)
    document = portal['document-1']


.. _content_get_state_example:

Get workflow state
------------------

To find out the current workflow state of your content, use the
:meth:`api.content.get_state` method.

.. code-block:: python

    from plone import api
    portal = api.portal.get()
    state = api.content.get_state(obj=portal['about'])

.. invisible-code-block: python

    self.assertEqual(state, 'private')


.. _content_transition_example:

Transition
----------

To transition your content to a new workflow state, use the
:meth:`api.content.transition` method.

.. code-block:: python

    from plone import api
    portal = api.portal.get()
    state = api.content.transition(obj=portal['about'], transition='publish')

.. invisible-code-block: python

    self.assertEqual(
        api.content.get_state(obj=portal['about']),
        'published'
    )


.. _content_get_view_example:

Get view
--------

To get a :class:`BrowserView` for your content, use :meth:`api.content.get_view`.

.. code-block:: python

    from plone import api
    portal = api.portal.get()
    view = api.content.get_view(
        name='plone',
        context=portal['about'],
        request=request,
    )

.. invisible-code-block: python

    self.assertEqual(view.__name__, u'plone')


Further reading
---------------

For more information on possible flags and usage options please see the full
:ref:`plone-api-content` specification.
