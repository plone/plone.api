.. admonition:: GitHub-only

    WARNING: If you are reading this on GitHub, DON'T! Read the documentation
    at `api.plone.org <http://api.plone.org/content.html>`_
    so you have working references and proper formatting.


.. module:: plone

.. _chapter_content:

Content
=======

.. _list_objects_example:

List folder content
-------------------

In order to retrieve the contents of a Plone folder or a folderish object you
use the ``plone.api.folder.list_objects()`` method. The following example lists
all Link objects with the ``some_folder`` folder object sorted by their title.
You can query by all indexes that are available in portal_catalog and sort by
all configured portal_catalog metadata. 

.. code-block:: python

    from plone import api
    portal = api.portal.get()

    api.create(container, type='Document', id='document', title='Document')
    api.create(container, type='Link', id='link', title='Link')

    objs = api.folder.list_objects(
        container=portal,
        content_filter={'portal_type': 'Link'},
        sort_on='sortable_title')

    assert objs[0].getId() == 'link'
    assert objs[0].Title() == 'Link'

    objs = api.folder.list_objects(
        container=portal,
        content_filter={'portal_type': 'Document'},
        sort_on='sortable_title')

    assert objs[0].getId() == 'document'
    assert objs[0].Title() == 'Document'

If your application does not need the full content objects and can work
with Zcatalog brains then you can use the sister method 
``plone.api.folder.list_brains()``:

.. code-block:: python

    from plone import api
    brains = api.folder.list_brains(
        container=portal,
        content_filter={'portal_type': 'Link'})

    assert objs[0].getId == 'link'
    assert objs[0].Title == 'Link'
