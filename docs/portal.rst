.. admonition:: GitHub-only

    WARNING: If you are reading this on GitHub, DON'T!
    Read the documentation at `docs.plone.org <http://docs.plone.org/develop/plone.api/docs/portal.html>`_
    so you have working references and proper formatting.


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

.. invisible-code-block: python

    self.assertEqual(portal.getPortalTypeName(), 'Plone Site')
    self.assertEqual(portal.getId(), 'plone')


.. _portal_get_navigation_root_example:

Get navigation root
-------------------

In multilingual or multi-site Plone installations you probably want to get the language-specific navigation root object,
not the top portal object.

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

Since we now have the portal object, it's easy to get the portal URL.

.. code-block:: python

    from plone import api
    url = api.portal.get().absolute_url()

.. invisible-code-block: python

    self.assertEqual(url, 'http://nohost/plone')


.. _portal_get_tool_example:

Get tool
--------

To get a portal tool easily, use :meth:`api.portal.get_tool` and pass in the name of the tool you need.

.. code-block:: python

    from plone import api
    catalog = api.portal.get_tool(name='portal_catalog')

.. invisible-code-block: python

    self.assertEqual(catalog.__class__.__name__, 'CatalogTool')


.. _portal_get_localized_time_example:

Get localized time
------------------

To display the date/time in a user-friendly way, localized to the user's preferred language, use :meth:`api.portal.get_localized_time`.

.. code-block:: python

    from plone import api
    from DateTime import DateTime
    today = DateTime()
    localized = api.portal.get_localized_time(datetime=today)

.. invisible-code-block: python

    # assert that the result is in fact a datetime
    self.assertEqual(DateTime(localized).__class__, DateTime)


.. _portal_get_default_language_example:

Get default language
--------------------

To get the default language, use :meth:`api.portal.get_default_language`.

.. code-block:: python

    from plone import api
    lang = api.portal.get_default_language()

.. invisible-code-block: python

    # assert that the result is 'en'
    self.assertEqual(lang, 'en')


.. _portal_get_current_language_example:

Get current language
--------------------

To get the currently negotiated language, use :meth:`api.portal.get_current_language`.

.. code-block:: python

    from plone import api
    lang = api.portal.get_current_language()

.. invisible-code-block: python

    # assert that the result is 'en'
    self.assertEqual(lang, 'en')


.. _portal_translate_example:

Translate
---------

To translate a message in a given language, use :meth:`api.portal.translate`.

.. code-block:: python

    from plone import api
    msg = api.portal.translate('Edited', lang='es')

.. invisible-code-block: python

    # assert that the translation is correct
    self.assertEqual(msg, u'Editado')


.. _portal_send_email_example:

Send E-Mail
-----------

To send an e-mail use :meth:`api.portal.send_email`:

.. invisible-code-block: python

    # Mock the mail host so we can test sending the email
    from plone import api
    from Products.CMFPlone.tests.utils import MockMailHost
    from Products.CMFPlone.utils import getToolByName
    from Products.MailHost.interfaces import IMailHost
    api.portal.PRINTINGMAILHOST_ENABLED = True

    mockmailhost = MockMailHost('MailHost')
    if not hasattr(mockmailhost, 'smtp_host'):
        mockmailhost.smtp_host = 'localhost'
    portal = api.portal.get()
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

If you need to add other fields not supported on send_email signature,
Python's standard `email module <https://docs.python.org/2.7/library/email.message.html#email.message.Message>`_ can also be used:

.. code-block:: python

    from email.mime.multipart import MIMEMultipart
    from email.mime.text import MIMEText

    message = MIMEMultipart()
    message.attach(MIMEText("One for you Bar!"))

    part = MIMEText('<xml></xml>', 'xml')
    part.add_header(
        'Content-Disposition',
        'attachment; filename="report.xml"'
    )
    message.attach(part)

    message['Reply-To'] = "community@plone.org"

    api.portal.send_email(
        recipient="bob@plone.org",
        sender="noreply@plone.org",
        subject="Trappist",
        body=message,
    )

.. invisible-code-block: python

    self.assertEqual(len(mailhost.messages), 2)

    msg = message_from_string(mailhost.messages[1])
    payloads = msg.get_payload()
    self.assertEqual(len(payloads), 2)
    self.assertEqual(msg['Reply-To'], 'community@plone.org')
    self.assertEqual(payloads[0].get_payload(), 'One for you Bar!')
    self.assertIn(
        'attachment; filename="report.xml',
        payloads[1]['Content-Disposition']
    )
    api.portal.PRINTINGMAILHOST_ENABLED = False
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

Plone comes with a package ``plone.app.registry`` that provides a common way to store configuration and settings.
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

One common pattern when using registry records is to define an interface with all the settings.
:meth:`api.portal.get_registry_record` also allows you to use this pattern.

.. invisible-code-block: python

    from plone.registry.interfaces import IRegistry
    from plone.api.tests.test_portal import IMyRegistrySettings

    registry = getUtility(IRegistry)
    registry.registerInterface(IMyRegistrySettings)
    records = registry.forInterface(IMyRegistrySettings)
    records.field_one = u'my text'

.. code-block:: python

    from plone import api
    api.portal.get_registry_record('field_one', interface=IMyRegistrySettings)

.. invisible-code-block: python

    self.assertEqual(
        api.portal.get_registry_record('field_one', interface=IMyRegistrySettings),
        u'my text'
    )

It is possible to provide a default value
that will be returned by :meth:`api.portal.get_registry_record`
if the queried record is not found.

.. code-block:: python

    from plone import api
    api.portal.get_registry_record('foo', interface=IMyRegistrySettings, default=u'bar')
    api.portal.get_registry_record('foo', default=u'baz')

.. invisible-code-block: python
    self.assertEqual(
        api.portal.get_registry_record(
            'foo',
            interface=IMyRegistrySettings,
            default=u'bar'
        ),
        u'bar',
    )
    self.assertEqual(
        api.portal.get_registry_record('foo', default=u'baz'),
        u'baz',
    )

.. _portal_set_registry_record_example:

Set plone.app.registry record
-----------------------------

:meth:`api.portal.set_registry_record` provides an easy way to change ``plone.app.registry`` configuration and settings.

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

:meth:`api.portal.set_registry_record` allows you to define an interface with all the settings.


.. invisible-code-block: python

    from plone.registry.interfaces import IRegistry
    from plone.api.tests.test_portal import IMyRegistrySettings

    registry = getUtility(IRegistry)
    registry.registerInterface(IMyRegistrySettings)
    records = registry.forInterface(IMyRegistrySettings)

.. code-block:: python

    from plone import api
    api.portal.set_registry_record('field_one', u'new value', interface=IMyRegistrySettings)

.. invisible-code-block: python

    self.assertEqual(
        api.portal.get_registry_record('field_one', interface=IMyRegistrySettings),
        u'new value'
    )

Further reading
---------------

For more information on possible flags and usage options please see the full :ref:`plone-api-portal` specification.
