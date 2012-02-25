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

a) api.create(portal.folder, 'foo',
       type='Document',
       attr1='abc',
       title='def')
b) portal.folder['foo'] = api.create(type='Document', attr...)

.. code-block:: python

   # create content
   # XXX What type of content are we creating here?
   site['foo'] = api.create_content(type='Folder', title='Foo')
   site['bar'] = api.create_content('Folder', title='Bar')
   site.bar['doc'] = api.create_content('Page', title='Doc')
   # XXX Other way?
   content = content.add_content(type, id, \*\*kw)

   print 'Output     text.'

.. invisible-code-block:: python

   :options: -ELLIPSIS, +NORMALIZE_WHITESPACE

   Output text.


Move content
------------

a) api.move(source=portal.someobj, target=portal.folder)
b) portal.folder['foo'] = portal.pop('someobj')

.. code-block:: python

   # move content (works)
   # XXX will this also trigger events?
   site.foo['doc'] = site.bar.pop('doc')

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

