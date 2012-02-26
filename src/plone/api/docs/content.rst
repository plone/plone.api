*******************************
:mod:`plone.api.content`
*******************************

:Author: Plone Foundation
:Version: |version|

.. module:: plone.api.content

.. topic:: Overview

   The :mod:`plone.api.content` provides CRUD methods for content objects and
   containers.

Manipulation of content objects
===============================

Create content
--------------

If you want to create content, use this method. The type attribute will
automatically decide which content type (dexterity, archetype, ...) should
be created.

.. code-block:: python

   from plone.api import content

   obj = content.create(type='Document',
                        id='myid',
                        title='This is a test document.')

.. invisible-code-block:: python

   self.assertEquals(obj.Title(), 'This is a test document')


Getting a content object
------------------------

This will get a content object by path.

.. code-block:: python

   from plone.api import content

   content.create(type='Document',
                  id='getme',
                  title='The title')
   obj = content.get(id='/getme')

.. invisible-code-block:: python

   self.assertEquals(obj.Title(), "The title")



Move content
------------

This is how you can move content around like in a file system.

.. code-block:: python

   from plone.api import content

   # Create some content
   news = content.create(type='Folder', id='news')
   contact = content.create(type='Folder', id='contact')
   content.create(container=news, 
                  type='Document',
                  id='aboutus',
                  title='About us')

   # Now move the 'aboutus' page over to 'contact'.
   aboutus = content.get(id='/news/aboutus')
   obj = content.move(source=aboutus, target=contact)

.. invisible-code-block:: python

   self.assertLength(news, 0)
   self.assertEquals(obj.Title(), 'About us')


Copy content
------------

To copy a content object, use this:

.. code-block:: python

   from plone.api import content
   from plone import api

   # Create some content
   copyme = content.create(type='Document', id='copyme')

   # Now make a copy of it. 
   obj = content.copy(source=copyme, id='thecopy')

.. invisible-code-block:: python

   self.assertNotEquals(obj, copyme)
   self.assertEquals(copyme.Title(), 'Copy me')
   self.assertEquals(obj.Title(), 'Copy me')


Delete content
--------------

Deleting content works like this:

.. code-block:: python

   from plone.api import content

   content.create(type='Document', id='deleteme')
   content.delete(object=content.get(id='deleteme'))

.. invisible-code-block:: python

   from plone import api
   self.assertNone(api.get_site().get(id='deleteme'))




Workflows
---------

Now, with the object you get from this API, you can call convenience methods
on it, like triggering a workflow transition.

.. code-block:: python

   from plone.api import content

   obj = content.create(type='Document', id='workflowme')
   old_state = content.get_state(obj=obj)

   content.transition(obj=obj, state='publish')
   new_state = content.get_state(obj=obj)
   
   content.transition(obj=new_obj, state=old_state)
   restored_state = content.get_state(obj=obj)

.. invisible-code-block:: python

   self.assertEquals(new_state, 'published')
   self.assertEquals(restored_state, old_state)

