Portal
======

.. _portal_url_example:

Get portal url
--------------

A shortcut to getting the portal's url is now always at hand.

.. code-block:: python

    from plone import api
    url = api.portal.url()

.. invisible-code-block:: python

    self.assertEqual(url, 'http://nohost/plone')


.. _portal_get_example:

Get portal object
-----------------

Getting the Plone site object goes like this:

.. code-block:: python

    from plone import api
    portal = api.portal.get()

.. invisible-code-block:: python

    self.assertEquals(portal.getPortalTypeName(), 'Plone Site')
    self.assertEquals(portal.getId(), 'plone')


.. _portal_get_tool_example:

Get tool
--------

To get a portal tool in a simple way, just use ``get_tool`` and pass in the
name of the tool you need.

.. code-block:: python

    from plone import api
    catalog = api.portal.get_tool(name='portal_catalog')

.. invisible-code-block:: python

    self.assertEqual(catalog.__class__.__name__, 'CatalogTool')


.. _portal_send_email_example:

Send E-Mail
-----------

To send an e-mail use ``send_email``:

.. Todo: Add example for creating a mime-mail

.. invisible-code-block:: python

    # Mock the mail host so we can test sending the email
    from plone import api
    from Products.CMFPlone.tests.utils import MockMailHost
    from Products.CMFPlone.utils import getToolByName
    from Products.MailHost.interfaces import IMailHost

    mockmailhost = MockMailHost('MailHost')
    portal = api.portal.get()
    portal.MailHost = mockmailhost
    sm = portal.getSiteManager()
    sm.registerUtility(component=mockmailhost, provided=IMailHost)
    mailhost = getToolByName(portal, 'MailHost')
    mailhost.reset()

.. code-block:: python

    api.portal.send_email(
        body="hello, bob",
        recipient="bob@plone.org",
        sender="admin@mysite.com",
        subject="hello world",
    )

.. invisible-code-block:: python

    self.assertEqual(len(mailhost.messages), 1)

    msg = mailhost.messages[0]
    self.assertTrue('To: bob@plone.org' in msg)
    self.assertTrue('From: admin@mysite.com' in msg)
    self.assertTrue('Subject: =?utf-8?q?hello_world' in msg)
    self.assertTrue('hello, bob' in msg)


.. _portal_show_message_example:

Show notification message
-------------------------

This is how to show a notification message to the user.

.. code-block:: python

    from plone import api
    api.portal.show_message(message='Blueberries!', request=self.request)

.. invisible-code-block:: python

    from Products.statusmessages.interfaces import IStatusMessage
    messages = IStatusMessage(request)
    show = messages.show()
    self.assertEquals(len(show), 1)
    self.assertTrue('Blueberries!' in show[0].message)


.. _portal_localized_time_example:

Localized time
--------------

To display a date/time in a user-friendly way, localized to the user's prefered
language, use the following:

.. code-block:: python

    # TODO: don't yet know how this will look
