Manipulation of content objects
===============================

Loading the API for a content object
------------------------------------

If you want to use plone.api for an existing object, simply call plone.api.content with
the object.

.. code-block:: python

   from plone import api
   content = api.content(context)

.. invisible-code-block:: python

   None

You can also load content by path (from the site root):

.. code-block:: python

   obj = api.get_content('/folder/folder/page')

.. invisible-code-block:: python

   self.assertEquals(obj.Title(), "?!")


Create content
--------------

.. warning ::

   This is for discussion - should we support version A or B?

.. note ::

   Version A

.. code-block:: python

   site = api.get_site()
   api.create(site, 'foo',
       type='Document',
       id='myid',
       title='This is a test document.')

.. note ::

   Version B

.. code-block:: python

   site = api.get_site()
   site['myid'] = api.create(
       type='Document',
       title='This is a test document.'')


.. invisible-code-block:: python

   self.assertEquals(site['myid'].Title(), 'This is a test document')


Move content
------------

.. warning ::

   This is for discussion - should we support version A or B?

.. note ::

   Version A

.. code-block:: python

   api.move(source=portal.someobj, target=portal.folder)

.. note ::

   Version B

.. code-block:: python

   # XXX will this also trigger events?
   portal.folder['foo'] = portal.pop('someobj')

.. invisible-code-block:: python

   None


Copy content
------------

a) api.copy(source=portal.someobj, target=portal.folder)
b) portal.folder['foo'] = api.copy(portal.someobj)

.. code-block:: python

   site.bar['test'] = api.copy(site.foo.doc)

.. invisible-code-block:: python

   None



Delete content
--------------

a) api.delete(portal.someobj)
b) del portal.folder['foo']

.. code-block:: python

   # delete content (works)
   # XXX will this also trigger events?
   del site.bar['test']

.. invisible-code-block:: python

   None


Workflows
---------

.. code-block:: python

   content.transition('publish')

.. invisible-code-block:: python

   None



Search content
--------------

.. code-block:: python

   api.search(\*\*catalog_search_params)

.. invisible-code-block:: python

   None

