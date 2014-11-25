.. admonition:: GitHub-only

    WARNING: If you are reading this on GitHub, DON'T! Read the documentation at `api.plone.org <http://api.plone.org/content.html>`_ so you have working references and proper formatting.


.. module:: plone

.. _chapter_content:

Content
=======

.. _content_create_example:

Create content
--------------

To add an object, you must first have a container in which to put it.
Get the portal object, it will serve nicely:

.. code-block:: python

    from plone import api
    portal = api.portal.get()

Create your new content item using the :meth:`api.content.create` method.
The type argument will decide which content type will be created.
Both Dexterity and Archetypes content types are supported.

.. code-block:: python

    from plone import api
    obj = api.content.create(
        type='Document',
        title='My Content',
        container=portal)

The ``id`` of the new object is automatically and safely generated from its ``title``.

.. code-block:: python

    assert obj.id == 'my-content'
    
.. _content_create_image_example:

Create image object
~~~~~~~~~~~~~~~~~~~

Creating an image is a two step process. First create 
an empty object then populate it with a binary "payload".

In this example, we'll add the image to the portal root:

.. code-block:: python

    from plone import api
    portal = api.portal.get()

Create the empty image using the :meth:`api.content.create` method.

.. code-block:: python

    from plone import api
    image = api.content.create(
        type='Image',
        title='My Image',
        container=portal)

Next populate the image with a binary "payload".

.. code-block:: python

    # doesn't matter how you retrieve the image "payload"
    # this example is hardcoded but it could just as
    # easily be a "payload" from a form or a url
    
    sample_payload = (
         'GIF89a\x10\x00\x10\x00\xd5\x00\x00\xff\xff\xff\xff\xff\xfe\xfc\xfd\xfd'
         '\xfa\xfb\xfc\xf7\xf9\xfa\xf5\xf8\xf9\xf3\xf6\xf8\xf2\xf5\xf7\xf0\xf4\xf6'
         '\xeb\xf1\xf3\xe5\xed\xef\xde\xe8\xeb\xdc\xe6\xea\xd9\xe4\xe8\xd7\xe2\xe6'
         '\xd2\xdf\xe3\xd0\xdd\xe3\xcd\xdc\xe1\xcb\xda\xdf\xc9\xd9\xdf\xc8\xd8\xdd'
         '\xc6\xd7\xdc\xc4\xd6\xdc\xc3\xd4\xda\xc2\xd3\xd9\xc1\xd3\xd9\xc0\xd2\xd9'
         '\xbd\xd1\xd8\xbd\xd0\xd7\xbc\xcf\xd7\xbb\xcf\xd6\xbb\xce\xd5\xb9\xcd\xd4'
         '\xb6\xcc\xd4\xb6\xcb\xd3\xb5\xcb\xd2\xb4\xca\xd1\xb2\xc8\xd0\xb1\xc7\xd0'
         '\xb0\xc7\xcf\xaf\xc6\xce\xae\xc4\xce\xad\xc4\xcd\xab\xc3\xcc\xa9\xc2\xcb'
         '\xa8\xc1\xca\xa6\xc0\xc9\xa4\xbe\xc8\xa2\xbd\xc7\xa0\xbb\xc5\x9e\xba\xc4'
         '\x9b\xbf\xcc\x98\xb6\xc1\x8d\xae\xbaFgs\x00\x00\x00\x00\x00\x00\x00\x00'
         '\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
         '\x00,\x00\x00\x00\x00\x10\x00\x10\x00\x00\x06z@\x80pH,\x12k\xc8$\xd2f\x04'
         '\xd4\x84\x01\x01\xe1\xf0d\x16\x9f\x80A\x01\x91\xc0ZmL\xb0\xcd\x00V\xd4'
         '\xc4a\x87z\xed\xb0-\x1a\xb3\xb8\x95\xbdf8\x1e\x11\xca,MoC$\x15\x18{'
         '\x006}m\x13\x16\x1a\x1f\x83\x85}6\x17\x1b $\x83\x00\x86\x19\x1d!%)\x8c'
         '\x866#\'+.\x8ca`\x1c`(,/1\x94B5\x19\x1e"&*-024\xacNq\xba\xbb\xb8h\xbeb'
         '\x00A\x00;'
         )
    
    image.setImage(sample_payload)
    
The following URLs have good examples of retrieving a binary image payload:
http://stackoverflow.com/questions/4664343/open-file-in-python-and-read-bytes
http://stackoverflow.com/questions/7391945/how-do-i-read-image-data-from-a-url-in-python

.. _content_get_example:

Get content object
------------------

There are several approaches to getting your content object.
Consider the following portal structure::

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


The following operations will get objects from the stucture above, including using :meth:`api.content.get`.

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
    
    # returns None if UID cannot be found in catalog
    not_found = api.content.get(UID='notfound')


.. invisible-code-block: python

    self.assertTrue(portal)
    self.assertTrue(blog)
    self.assertTrue(about)
    self.assertTrue(conference)
    self.assertTrue(sprint)
    self.assertTrue(team)
    self.assertEquals(not_found, None)


.. _content_find_example:

Find content objects
--------------------

You can use the *catalog* to search for content.
Here is a simple example:

.. code-block:: python

    from plone import api
    catalog = api.portal.get_tool(name='portal_catalog')
    documents = catalog(portal_type='Document')

.. invisible-code-block: python
    self.assertEqual(catalog.__class__.__name__, 'CatalogTool')
    self.assertEqual(len(documents), 3)

More information about how to use the catalog may be found in the `Plone Documentation <http://docs.plone.org/develop/plone/searching_and_indexing/index.html>`_.
Note that the catalog returns *brains* (metadata stored in indexes) and not objects.
However, calling ``getObject()`` on brains does in fact give you the object.

.. code-block:: python

    document_brain = documents[0]
    document_obj = document_brain.getObject()
    assert document_obj.__class__.__name__ == 'ATDocument'

.. _content_get_uuid_example:

Get content object UUID
-----------------------

A Universally Unique IDentifier (UUID) is a unique, non-human-readable identifier for a content object which stays on the object even if the object is moved.

Plone uses UUIDs for storing references between content and for linking by UIDs, enabling persistent links.

To get the UUID of any content object use :meth:`api.content.get_uuid`.
The following code gets the UUID of the ``contact`` document.

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

To move content around the portal structure defined above use the :meth:`api.content.move` method.
The code below moves the ``contact`` item (with all it contains) out of the folder ``about`` and into the Plone portal root.

.. code-block:: python

    from plone import api
    portal = api.portal.get()
    contact = portal['about']['contact']

    api.content.move(source=contact, target=portal)

.. invisible-code-block: python

    self.assertFalse(portal['about'].get('contact'))
    self.assertTrue(portal['contact'])

Actually, ``move`` behaves like a filesystem move.
If you pass it an ``id`` argument the object will have that new ID in it's new home.
By default it will retain its original ID.

.. _content_rename_example:

Rename content
--------------

To rename a content object (change its ID), use the :meth:`api.content.rename` method.

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

Note that the new object will have the same ID as the old object (unless otherwise stated).
This is not a problem, since the new object is in a different container.

.. invisible-code-block: python

    assert portal['events']['training'].id == 'training'
    assert portal['training'].id == 'training'


You can also set ``target`` to source's container and set ``safe_id=True``.
This will duplicate your content object in the same container and assign it a new, non-conflicting ID.

.. code-block:: python

    api.content.copy(source=portal['training'], target=portal, safe_id=True)
    new_training = portal['copy_of_training']

.. invisible-code-block: python

    self.assertTrue(portal['training'])  # old object remains
    self.assertTrue(portal['copy_of_training'])


.. _content_delete_example:

Delete content
--------------

To delete a content object, pass the object to the :meth:`api.content.delete` method:

.. code-block:: python

    from plone import api
    portal = api.portal.get()
    api.content.delete(obj=portal['copy_of_training'])

.. invisible-code-block: python

    self.assertFalse(portal.get('copy_of_training'))


.. _content_manipulation_with_safe_id_option:

Content manipulation with the `safe_id` option
----------------------------------------------

When manipulating content with :meth:`api.content.create`, :meth:`api.content.move` or :meth:`api.content.copy` the `safe_id` flag is disabled by default.
This means the uniqueness of IDs will be enforced.
If another object with the same ID is already present in the target container these API methods will raise an error.

However, if the `safe_id` option is enabled, a non-conflicting id will be generated.

.. invisible-code-block: python

    api.content.create(container=portal, type='Document', id='document', safe_id=True)

.. code-block:: python

    api.content.create(container=portal, type='Document', id='document', safe_id=True)
    document = portal['document-1']


.. _content_get_state_example:

Get workflow state
------------------

To find out the current workflow state of your content, use the :meth:`api.content.get_state` method.

.. code-block:: python

    from plone import api
    portal = api.portal.get()
    state = api.content.get_state(obj=portal['about'])

.. invisible-code-block: python

    self.assertEqual(state, 'private')


.. _content_transition_example:

Transition
----------

To transition your content to a new workflow state, use the :meth:`api.content.transition` method.

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

For more information on possible flags and usage options please see the full :ref:`plone-api-content` specification.
