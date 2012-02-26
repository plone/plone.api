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
   api.create(site,
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
       title='This is a test document.')


.. invisible-code-block:: python

   self.assertEquals(site['myid'].Title(), 'This is a test document')


Getting a content object
------------------------

This will get a content object by path.

.. warning ::

   This is for discussion - should we support version A or B?

.. note ::

   Version A (command line style)

.. code-block:: python

   from plone import api

   api.create(type='Document',
       id='getme',
       title='The title')
   obj = api.get_content('/getme')

.. invisible-code-block:: python

   self.assertEquals(obj.Title(), "The title")

.. note ::

   Version B (python dict style)

.. code-block:: python

   from plone import api

   site = api.get_site()
   site['getme'] = api.create(
       type='Document',
       title='The title')
   obj = site['getme']

.. invisible-code-block:: python

   self.assertEquals(obj.Title(), "The title")


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
   api.create(type='Folder', id='news')
   api.create(type='Folder', id='contact')
   api.create(parent=api.get_content('/news'), type='Document', id='aboutus')

   # Now move the 'aboutus' page over to 'contact'.
   aboutus = api.get_content('/news/aboutus')
   contact = api.get_content('/contact')
   api.move(source=aboutus, target=contact)

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

To copy a content object, use this:

.. warning ::

   This is for discussion - should we support version A or B?

.. note ::

   Version A (command line style)

.. code-block:: python

   from plone import api

   # Create some content
   copyme = api.create(type='Document', id='copyme')

   api.copy(source=copyme, target=api.get_site(), id='thecopy')

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

Deleting content works like this:

.. warning ::

   This is for discussion - should we support version A or B?

.. note ::

   Version A (command line style)

.. code-block:: python

   from plone import api

   api.create(type='Document', id='deleteme')
   api.delete(api.get_content('deleteme'))

.. note ::

   Version B (python dict style)

.. code-block:: python

   from plone import api

   site = api.get_site()
   site['deleteme'] = api.create(type='Document')
   del site['deleteme']

.. invisible-code-block:: python

   self.assertNone(site.get('deleteme'))


Search content
--------------

Searching content works by utilizing the portal_catalog tool so you can use
the same arguments.
The search returns brains.

.. warning ::

   This is for discussion - should we support version A or B?

.. note ::

   Version A (command line style)

.. code-block:: python

   from plone import api

   api.create(type='Document', id='findme', title='FIND ME')
   brains = api.search(title='FIND ME')

.. invisible-code-block:: python

   self.assertLength(brains, 1)
   self.assertEquals(brains.Title, 'FIND ME')

.. note ::

   Version B (python dict style)

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

.. warning ::

   This is for discussion - should we support version A or B?

.. note ::

   Version A (command line style)

.. code-block:: python

   from plone import api

   api.create(type='Document', id='workflowme')
   api.transition(api.get_content('workflowme'), 'publish')

.. invisible-code-block:: python

   self.assertEquals(api.state(site['workflowme'], 'published'))

.. note ::

   Version B (python dict style)

.. code-block:: python

   from plone import api

   site['workflowme'] = api.create(type='Document')
   api.transition(site['workflowme'], 'publish')

.. invisible-code-block:: python

   self.assertEquals(api.state(site['workflowme'], 'published'))

To see the current status, use this:

.. warning ::

   This is for discussion - should we support version A or B?

.. note ::

   Version A (command line style)

.. code-block:: python

   state = api.state(api.get_content('workflowme'))

.. note ::

   Version B (python dict style)

.. code-block:: python

   state = api.state(site['workflowme'])

