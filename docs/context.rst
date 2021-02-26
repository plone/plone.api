.. admonition:: GitHub-only

    WARNING: If you are reading this on GitHub, DON'T!
    Read the documentation at `docs.plone.org <http://docs.plone.org/develop/plone.api/docs/content.html>`_
    so you have working references and proper formatting.


.. module:: plone

.. _chapter_context:

=======
Context
=======

.. _context_current_page_url_example:

Get current page url
====================

The URL to the current page, including template and query string:

.. code-block:: python

    from plone import api
    url = api.context.current_page_url(context, request)


.. _context_view_template_id_example:

Get view template id
====================

.. invisible-code-block: python

    api.content.create(container=about, type='Document', id='contact')

To get a :class:`BrowserView` for your content, use :meth:`api.content.get_view`.
The current id of the view-template, use :meth:`api.context.view_template_id`.

.. code-block:: python

    from plone import api
    contact_page = api.content.get('/contact')
    id = api.context.view_template_id(
        context=contact_page,
        request=request,
    )

.. invisible-code-block: python

    self.assertEqual(id, u'template-document_view')




Further reading
===============

For more information on possible flags and usage options please see the full :ref:`plone-api-context` specification.
