Manipulation of content objects
===============================

Loading the API for a content object
------------------------------------

.. testcode::

   content = api.content(context)
   context = api.get_content('/folder/folder/page')

.. testoutput::

   None

Create content
--------------

a) api.create(portal.folder, 'foo',
       type='Document',
       attr1='abc',
       title='def')
b) portal.folder['foo'] = api.create(type='Document', attr...)

.. testcode::

   # create content
   # XXX What type of content are we creating here?
   site['foo'] = api.create_content(type='Folder', title='Foo')
   site['bar'] = api.create_content('Folder', title='Bar')
   site.bar['doc'] = api.create_content('Page', title='Doc')
   # XXX Other way?
   content = content.add_content(type, id, \*\*kw)

   print 'Output     text.'

.. testoutput::

   :options: -ELLIPSIS, +NORMALIZE_WHITESPACE

   Output text.


Move content
------------

a) api.move(source=portal.someobj, target=portal.folder)
b) portal.folder['foo'] = portal.pop('someobj')

.. testcode::

   # move content (works)
   # XXX will this also trigger events?
   site.foo['doc'] = site.bar.pop('doc')

.. testoutput::

   None


Copy content
------------

a) api.copy(source=portal.someobj, target=portal.folder)
b) portal.folder['foo'] = api.copy(portal.someobj)

.. testcode::

   site.bar['test'] = api.copy(site.foo.doc)

.. testoutput::

   None



Delete content
--------------

a) api.delete(portal.someobj)
b) del portal.folder['foo']

.. testcode::

   # delete content (works)
   # XXX will this also trigger events?
   del site.bar['test']

.. testoutput::

   None


Workflows
---------

.. testcode::

   content.transition('publish')

.. testoutput::

   None



Search content
--------------

.. testcode::

   api.search(\*\*catalog_search_params)

.. testoutput::

   None

