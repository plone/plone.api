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

   Version A (command line style)

.. code-block:: python

   from plone import api
   site = api.get_site()
   api.create(site, 'foo',
       type='Document',
       id='myid',
       title='This is a test document.')

.. note ::

   Version B (python dict style)

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

That's how you can move content around like in a file system.

.. warning ::

   This is for discussion - should we support version A or B?

.. note ::

   Version A (command line style)

.. code-block:: python

   from plone import api

   # Create some content
   site = api.get_site()
   api.create(site, type='Folder', id='news')
   api.create(site, type='Folder', id='contact')
   api.create(site['news'], type='Document', id='aboutus')

   # Now move the 'aboutus' page over to 'contact'.
   api.move(source=site['news']['aboutus'], target=site['contact'])

.. note ::

   Version B (python dict style)

.. code-block:: python

   from plone import api

   # Create some content
   site = api.get_site()
   site['news'] = api.create(type='Folder')
   site['contact'] = api.create(type='Folder')
   site['news']['aboutus'] = api.create(type='Document', title='About us')

   # Now move the 'aboutus' page over to 'contact'.
   site['contact']['aboutus'] = site['news'].pop('aboutus')

.. invisible-code-block:: python

   self.assertLength(site['news'], 0)
   self.assertEquals(site['contact']['aboutus'].Title(), 'About us')


Copy content
------------

To copy a content object, use that:

.. warning ::

   This is for discussion - should we support version A or B?

.. note ::

   Version A (command line style)

.. code-block:: python

   from plone import api

   # Create some content
   site = api.get_site()
   api.create(site, type='Document', id='copyme')

   api.copy(source=site['copyme'], target=site, id='thecopy')

.. note ::

   Version B (python dict style)

.. code-block:: python

   from plone import api

   # Create some content
   site = api.get_site()
   site['copyme'] = api.create(type='Document', title='Copy me')

   site['thecopy'] = api.copy(site['copyme'])

.. invisible-code-block:: python

   self.assertEquals(site['copyme'].Title(), 'Copy me')
   self.assertEquals(site['thecopy'].Title(), 'Copy me')


Delete content
--------------

Deleting content works like that:

.. warning ::

   This is for discussion - should we support version A or B?

.. note ::

   Version A (command line style)

.. code-block:: python

   from plone import api

   site = api.get_site()
   site['deleteme'] = api.create(type='Document')
   api.delete(site['deleteme'])

.. note ::

   Version B (python dict style)

.. code-block:: python

   from plone import api

   site = api.get_site()
   site['deleteme'] = api.create(type='Document')
   del site['deleteme']

.. invisible-code-block:: python

   self.assertNone(site.get('deleteme'))


Getting a content object
------------------------

This will get a content object by path.

.. code-block:: python

   from plone import api

   site = api.get_site()
   site['getme'] = api.create(type='Document', title='The title')
   obj = api.get_content('/getme')

.. invisible-code-block:: python

   self.assertEquals(obj.Title(), "The title")


Search content
--------------

Searching content works by utilizing the portal_catalog tool so you can use
the same arguments.
The search returns brains.

.. code-block:: python

   from plone import api
   site['findme'] = api.create(type='Document', title='FIND ME')
   brains = api.search(title='FIND ME')

.. invisible-code-block:: python

   self.assertLength(brains, 1)
   self.assertEquals(brains.Title, 'FIND ME')


Workflows
---------

Now, with the API'd content, you can call convenience methods on it, like
triggering a workflow transition.

.. code-block:: python

   from plone import api
   site['workflowme'] = api.create(type='Document')
   api.transition(site['workflowme'], 'publish')

.. invisible-code-block:: python

   self.assertEquals(api.state(site['workflowme'], 'published')

To see the current status, use this:

.. code-block:: python

   state = api.state(site['workflowme'])


