Manipulation of content objects
===============================

Create content
--------------

If you want to create content, use this method. The type attribute will
automatically decide which content type (dexterity, archetype, ...) should
be created.

.. warning ::

   This is for discussion - should we support version A or B?

.. note ::

   Version A

.. code-block:: python

   from plone import api
   site = api.get_site()
   api.create(site, 'foo',
       type='Document',
       id='myid',
       title='This is a test document.')

.. note ::

   Version B

.. code-block:: python

   from plone import api
   site = api.get_site()
   site['myid'] = api.create(
       type='Document',
       title='This is a test document.'')


.. invisible-code-block:: python

   self.assertEquals(site['myid'].Title(), 'This is a test document')


Move content
------------

To move a content object around, use this.

.. warning ::

   This is for discussion - should we support version A or B?

.. note ::

   Version A (command line style)

.. code-block:: python

   from plone import api
   api.move(source=portal.someobj, target=portal.folder)

.. note ::

   Version B (python dict style)

.. code-block:: python

   # XXX will this also trigger events?
   portal.folder['foo'] = portal.pop('someobj')

.. invisible-code-block:: python

   None


Copy content
------------

To copy a content object, use that:

.. warning ::

   This is for discussion - should we support version A or B?

.. note ::

   Version A (command line style)

.. code-block:: python

   api.copy(source=portal.someobj, target=portal.folder)

.. note ::

   Version B (python dict style)

.. code-block:: python

   site.bar['test'] = api.copy(site.foo.doc)

.. invisible-code-block:: python

   None



Delete content
--------------

.. warning ::

   This is for discussion - should we support version A or B?

.. note ::

   Version A (command line style)

.. code-block:: python

    api.delete(portal.someobj)

.. note ::

   Version B (python dict style)

.. code-block:: python

   # XXX will this also trigger events?
   del site.bar['test']

.. invisible-code-block:: python

   None


Loading the API for a content object
------------------------------------

If you want to use plone.api for an existing object, simply call plone.api.content with
the object.

.. code-block:: python

   from plone import api
   obj = api.content(context)

.. invisible-code-block:: python

   None

You can also load content by path (from the site root):

.. code-block:: python

   obj = api.get_content('/folder/folder/page')

.. invisible-code-block:: python

   self.assertEquals(obj.Title(), "?!")


Workflows
---------

Now, with the API'd content, you can call convenience methods on it, like
triggering a workflow transition.

.. code-block:: python

   content.transition('publish')

.. invisible-code-block:: python

   self.assertEquals(content.state, 'published')

To see the current status, use this:

.. code-block:: python

   state = content.state



Search content
--------------

.. code-block:: python

   api.search(\*\*catalog_search_params)

.. invisible-code-block:: python

   None

