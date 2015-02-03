.. admonition:: GitHub-only

    WARNING: If you are reading this on GitHub, DON'T! Read the documentation at `api.plone.org <http://api.plone.org/portal.html>`_ so you have working references and proper formatting.


.. module:: plone

.. _chapter_portal:

Portal
======

.. contents:: :local:


.. _portal_get_example:

Get portal object
-----------------

Getting the Plone portal object is easy with :meth:`api.portal.get`.

.. code-block:: python

    from plone import api
    portal = api.portal.get()

.. invisible-code-block: python

    self.assertEqual(portal.getPortalTypeName(), 'Plone Site')
    self.assertEqual(portal.getId(), 'plone')


.. _portal_get_navigation_root_example:

Get navigation root
-------------------

In multi-lingual or multi-site Plone installations you probably want to get the language-specific navigation root object, not the top portal object.
You do this with :meth:`api.portal.get_navigation_root()`.

Assuming there is a document ``english_page`` in a folder ``en``, which is the navigation root:

.. invisible-code-block: python

    from plone import api
    from plone.app.layout.navigation.interfaces import INavigationRoot
    from zope.interface import alsoProvides

    portal = api.portal.get()
    english_folder = api.content.create(
        type='Folder',
        title='en',
        container=portal,
    )
    alsoProvides(english_folder, INavigationRoot)
    english_page = api.content.create(
        type='Document',
        title='English Page',
        container=english_folder,
    )

.. code-block:: python

    from plone import api
    nav_root = api.portal.get_navigation_root(english_page)

.. invisible-code-block: python

    self.assertEqual(nav_root.id, 'en')

returns the folder ``en``. If the folder ``en`` is not a navigation root it would return the portal.

Get portal url
--------------

Since we now have the portal object, it's easy to get the portal url.

.. code-block:: python

    from plone import api
    url = api.portal.get().absolute_url()

.. invisible-code-block: python

    self.assertEqual(url, 'http://nohost/plone')


.. _portal_get_tool_example:

Get tool
--------

To get a portal tool in a simple way, just use :meth:`api.portal.get_tool` and pass in the name of the tool you need.

.. code-block:: python

    from plone import api
    catalog = api.portal.get_tool(name='portal_catalog')

.. invisible-code-block: python

    self.assertEqual(catalog.__class__.__name__, 'CatalogTool')


.. _portal_get_localized_time_example:

Get localized time
------------------

To display the date/time in a user-friendly way, localized to the user's prefered language, use :meth:`api.portal.get_localized_time`.

.. code-block:: python

    from plone import api
    from DateTime import DateTime
    today = DateTime()
    localized = api.portal.get_localized_time(datetime=today)

.. invisible-code-block: python

    # assert that the result is in fact a datetime
    self.assertEqual(DateTime(localized).__class__, DateTime)


.. _portal_send_email_example:

Send E-Mail
-----------

To send an e-mail use :meth:`api.portal.send_email`:

.. Todo: Add example for creating a mime-mail

.. invisible-code-block: python

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

.. invisible-code-block: python

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

With :meth:`api.portal.show_message` you can show a notification message to the user.

.. code-block:: python

    from plone import api
    api.portal.show_message(message='Blueberries!', request=request)

.. invisible-code-block: python

    from Products.statusmessages.interfaces import IStatusMessage
    messages = IStatusMessage(request)
    show = messages.show()
    self.assertEqual(len(show), 1)
    self.assertTrue('Blueberries!' in show[0].message)


.. _portal_get_registry_record_example:

Get plone.app.registry record
-----------------------------

Plone comes with a package ``plone.app.registry`` that provides a common way to store various configuration and settings.
:meth:`api.portal.get_registry_record` provides an easy way to access these.

.. invisible-code-block: python

    from plone.registry.interfaces import IRegistry
    from plone.registry.record import Record
    from plone.registry import field
    from zope.component import getUtility
    registry = getUtility(IRegistry)
    registry.records['my.package.someoption'] = Record(field.Bool(
            title=u"Foo"))
    registry['my.package.someoption'] = True

.. code-block:: python

    from plone import api
    api.portal.get_registry_record('my.package.someoption')

.. invisible-code-block: python

    self.assertTrue(api.portal.get_registry_record('my.package.someoption'))


.. _portal_set_registry_record_example:

Set plone.app.registry record
-----------------------------

Plone comes with a package ``plone.app.registry`` that provides a common way to store various configuration and settings.
:meth:`api.portal.set_registry_record` provides an easy way to change these.

.. invisible-code-block: python

    from plone.registry.interfaces import IRegistry
    from plone.registry.record import Record
    from plone.registry import field
    from zope.component import getUtility
    registry = getUtility(IRegistry)
    registry.records['my.package.someoption'] = Record(field.Bool(
            title=u"Foo"))
    registry['my.package.someoption'] = True

.. code-block:: python

    from plone import api
    api.portal.set_registry_record('my.package.someoption', False)

.. invisible-code-block: python

    self.assertFalse(registry['my.package.someoption'])


Further reading
---------------

For more information on possible flags and usage options please see the full :ref:`plone-api-portal` specification.
