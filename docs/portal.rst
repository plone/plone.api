.. line-block::

    WARNING: If you are reading this on GitHub, DON'T! Read it on ReadTheDocs:
    http://ploneapi.readthedocs.org/en/latest/portal.html so you have working
    references and proper formatting.


.. module:: plone

.. _chapter_portal:

Portal
======

.. _portal_get_example:

Get portal object
-----------------

Getting the Plone portal object is easy with :meth:`api.portal.get`.

.. code-block:: python

    from plone import api
    portal = api.portal.get()

.. invisible-code-block:: python

    self.assertEquals(portal.getPortalTypeName(), 'Plone Site')
    self.assertEquals(portal.getId(), 'plone')


.. _portal_get_navigation_root_example:

Get navigation root
-------------------

In multi-lingual Plone installations you probably want to get the
language-specific navigation root object, not the top portal object. You do this with
:meth:`api.portal.get_navigation_root()`.

Assuming there is a document ``english_page`` in a folder ``en``, which is the navigation root:

.. invisible-code-block:: python

    from plone import api
    from plone.app.layout.navigation.interfaces import INavigationRoot
    from zope.interface import alsoProvides

    portal = api.portal.get()
    english_folder = api.content.create(
        type='Folder',
        title='en',
        container=portal)
    alsoProvides(english_folder, INavigationRoot)
    english_page = api.content.create(
        type='Document',
        title='English Page',
        container=english_folder)

.. code-block:: python

    from plone import api
    nav_root = api.portal.get_navigation_root(english_page)

.. invisible-code-block:: python

    self.assertEquals(nav_root.id, 'en')

returns the folder ``en``. If the folder ``en`` is not a navigation root it would return the portal.

Get portal url
--------------

Since we now have the portal object, it's easy to get the portal url.

.. code-block:: python

    from plone import api
    url = api.portal.get().absolute_url()

.. invisible-code-block:: python

    self.assertEqual(url, 'http://nohost/plone')


.. _portal_get_tool_example:

Get tool
--------

To get a portal tool in a simple way, just use :meth:`api.portal.get_tool` and
pass in the name of the tool you need.

.. code-block:: python

    from plone import api
    catalog = api.portal.get_tool(name='portal_catalog')

.. invisible-code-block:: python

    self.assertEqual(catalog.__class__.__name__, 'CatalogTool')


.. _portal_get_localized_time_example:

Get localized time
------------------

To display the date/time in a user-friendly way, localized to the user's
prefered language, use :meth:`api.portal.get_localized_time`.

.. code-block:: python

    from plone import api
    from DateTime import DateTime
    today = DateTime()
    api.portal.get_localized_time(datetime=today)

.. invisible-code-block:: python

    result = api.portal.get_localized_time(
        datetime=DateTime(1999, 12, 31, 23, 59))
    self.assertEqual(result, 'Dec 31, 1999')


.. _portal_send_email_example:

Send E-Mail
-----------

To send an e-mail use :meth:`api.portal.send_email`:

.. Todo: Add example for creating a mime-mail

.. invisible-code-block:: python

    # Mock the mail host so we can test sending the email
    from plone import api
    from Products.CMFPlone.tests.utils import MockMailHost
    from Products.CMFPlone.utils import getToolByName
    from Products.MailHost.interfaces import IMailHost

    mockmailhost = MockMailHost('MailHost')
    if not hasattr(mockmailhost, 'smtp_host'):
        mockmailhost.smtp_host = 'localhost'
    portal = api.portal.get()
    portal._updateProperty('email_from_address', 'sender@example.org')
    portal.MailHost = mockmailhost
    sm = portal.getSiteManager()
    sm.registerUtility(component=mockmailhost, provided=IMailHost)
    mailhost = getToolByName(portal, 'MailHost')
    mailhost.reset()

.. code-block:: python

    from plone import api
    api.portal.send_email(
        recipient="bob@plone.org",
        sender="noreply@plone.org",
        subject="Trappist",
        body="One for you Bob!",
    )

.. invisible-code-block:: python

    self.assertEqual(len(mailhost.messages), 1)

    from email import message_from_string
    msg = message_from_string(mailhost.messages[0])
    self.assertEqual(msg['To'], 'bob@plone.org')
    self.assertEqual(msg['From'], 'noreply@plone.org')
    self.assertEqual(msg['Subject'], '=?utf-8?q?Trappist?=')
    self.assertEqual(msg.get_payload(), 'One for you Bob!')
    mailhost.reset()


.. _portal_show_message_example:

Show notification message
-------------------------

With :meth:`api.portal.show_message` you can show a notification message to
the user.

.. code-block:: python

    from plone import api
    api.portal.show_message(message='Blueberries!', request=request)

.. invisible-code-block:: python

    from Products.statusmessages.interfaces import IStatusMessage
    messages = IStatusMessage(request)
    show = messages.show()
    self.assertEquals(len(show), 1)
    self.assertTrue('Blueberries!' in show[0].message)


.. _portal_get_registry_record_example:

Get plone.app.registry record
-----------------------------

Plone comes with a package ``plone.app.registry`` that provides a common way to
store various configuration and settings. The
:meth:`api.portal.get_registry_record` provides an easy way to access these
records.

.. code-block:: python

    from plone import api
    # Not implemented yet
