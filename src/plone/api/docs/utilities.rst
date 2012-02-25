Utilities
=========

Getting the plone site
----------------------

Getting the Plone site object goes like this:

.. code-block:: python

    from plone import api
    site = api.get_site()

.. invisible-code-block:: python

    self.assertEquals(site.getPortalTypeName(), 'Plone Site')
    self.assertEquals(site.getId(), 'plone')


Getting the current request
---------------------------

The request will be fetched from a thread local.

.. code-block:: python

    from plone import api
    request = api.get_request()

.. invisible-code-block:: python

    from ZPublisher.HTTPRequest import HTTPRequest
    self.assertTrue(isinstance(request, HTTPRequest))
    self.assertEqual(request.getURL(), 'http://nohost')


Sending an E-Mail
-----------------

To send an e-mail just use send_email:

.. Todo: Add example for creating a mime-mail

.. code-block::

   api.send_email(
       subject="hello world",
       sender="admin@mysite.com",
       recipients=["arthur.dent@gmail.com"],
       body="hello, arthur",
   )

.. invisible-code-block::

   None

