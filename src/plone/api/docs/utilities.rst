Utilities
=========

.. _get_site_url_example:

Get site url
------------

A shortcut to getting the site's url is now always at hand.

.. code-block:: python

    from plone import api
    url = api.get_site_url()

.. invisible-code-block:: python

    self.assertEqual(url, 'http://nohost')


.. _get_site_example:

Get site object
---------------

Getting the Plone site object goes like this:

.. code-block:: python

    from plone import api
    site = api.get_site()

.. invisible-code-block:: python

    self.assertEquals(site.getPortalTypeName(), 'Plone Site')
    self.assertEquals(site.getId(), 'plone')


.. _get_request_example:

Get current request
-------------------

The request will be fetched from a `thread-local  <http://readthedocs.org/docs/collective-docs/en/latest/persistency/lifecycle.html?highlight=thread-local>`_.

.. code-block:: python

    from plone import api
    request = api.get_request()

.. invisible-code-block:: python

    from ZPublisher.HTTPRequest import HTTPRequest
    self.assertTrue(isinstance(request, HTTPRequest))
    self.assertEqual(request.getURL(), 'http://nohost')


.. _get_tool_example:

Get tool
--------

To get a portal tool in a simple way, just use ``get_tool`` and pass in the
name of the tool you need.

.. code-block:: python

    from plone import api
    catalog = api.get_tool(name='portal_catalog')

.. invisible-code-block:: python

    self.assertEqual(catalog.__class__.__name__, 'CatalogTool')


.. _show_message_example:

Show notification message
-------------------------

This is how to show a notification message to the user.

.. code-block:: python

    from plone import api
    api.show_message(message='Blueberries rock!')

.. invisible-code-block:: python

    # TODO: how to test this?


.. _send_email_example:

Senda E-Mail
------------

To send an e-mail just use send_email:

.. Todo: Add example for creating a mime-mail

.. invisible-code-block:: python

    # Mock the mail host so we can test sending the email
    from plone import api
    from Products.CMFPlone.tests.utils import MockMailHost
    from Products.CMFPlone.utils import getToolByName
    from Products.MailHost.interfaces import IMailHost

    mockmailhost = MockMailHost('MailHost')
    site = api.get_site()
    site.MailHost = mockmailhost
    sm = site.getSiteManager()
    sm.registerUtility(component=mockmailhost, provided=IMailHost)
    mailhost = getToolByName(site, 'MailHost')
    mailhost.reset()

.. code-block:: python

    api.send_email(
        body="hello, bob",
        recipient="bob@plone.org",
        sender="admin@mysite.com",
       subject="hello world",
    )

.. invisible-code-block:: python
    # test email
    self.assertEqual(len(mailhost.messages), 1)

    msg = mailhost.messages[0]

    self.assertTrue('To: bob@plone.org' in msg)
    self.assertTrue('From: admin@mysite.com' in msg)
    self.assertTrue('Subject: =?utf-8?q?hello_world' in msg)
    self.assertTrue('hello, bob' in msg)
