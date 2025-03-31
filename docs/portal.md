---
myst:
  html_meta:
    "description": "Access tools and global settings. Send e-mails and raise notifications."
    "property=og:description": "Access tools and global settings. Send e-mails and raise notifications."
    "property=og:title": "Portal"
    "keywords": "Plone, development, API, global, task, "
---

```{eval-rst}
.. currentmodule:: plone.api.portal
```
% The Sphinx directive `currentmodule` is used to both run `code-block` examples via [Manuel](https://manuel.readthedocs.io/en/latest/#code-blocks-1) and to avoid duplicating an index entry that is already provided by its counterpart in `docs/api/*.md`.

(chapter-portal)=

# Portal

(portal-get-example)=

## Get portal object

Getting the Plone portal object is easy with {meth}`api.portal.get`.

```python
from plone import api
portal = api.portal.get()
```

% invisible-code-block: python
%
% self.assertEqual(portal.getPortalTypeName(), 'Plone Site')
% self.assertEqual(portal.getId(), 'plone')

(portal-get-navigation-root-example)=

## Get navigation root

In multilingual or multi-site Plone installations, you probably want to get the language-specific navigation root object, not the top portal object.

You do this with {meth}`api.portal.get_navigation_root()`.

Assuming there is a document `english_page` in a folder `en`, which is the navigation root:

% invisible-code-block: python
%
% from plone import api
% from plone.base.interfaces import INavigationRoot
% from zope.interface import alsoProvides
%
% portal = api.portal.get()
% english_folder = api.content.create(
%     type='Folder',
%     title='en',
%     container=portal,
% )
% alsoProvides(english_folder, INavigationRoot)
% english_page = api.content.create(
%     type='Document',
%     title='English Page',
%     container=english_folder,
% )

```python
from plone import api
nav_root = api.portal.get_navigation_root(english_page)
```

% invisible-code-block: python
%
% self.assertEqual(nav_root.id, 'en')

Returns the folder `en`. If the folder `en` is not a navigation root, it would return the portal.

## Get portal url

Since we now have the portal object, it's easy to get the portal URL.

```python
from plone import api
url = api.portal.get().absolute_url()
```

% invisible-code-block: python
%
% self.assertEqual(url, 'http://nohost/plone')

(portal-get-tool-example)=

## Get tool

To get a portal tool easily, use {meth}`api.portal.get_tool` and pass in the name of the tool you need.

```python
from plone import api
catalog = api.portal.get_tool(name='portal_catalog')
```

% invisible-code-block: python
%
% self.assertEqual(catalog.__class__.__name__, 'CatalogTool')

(portal-get-localized-time-example)=

## Get localized time

To display the date/time in a user-friendly way, localized to the user's preferred language, use {meth}`api.portal.get_localized_time`.

```python
from plone import api
from DateTime import DateTime
today = DateTime()
localized = api.portal.get_localized_time(datetime=today)
```

% invisible-code-block: python
%
% # assert that the result is in fact a datetime
% self.assertEqual(DateTime(localized).__class__, DateTime)

(portal-get-default-language-example)=

## Get default language

To get the default language, use {meth}`api.portal.get_default_language`.

```python
from plone import api
lang = api.portal.get_default_language()
```

% invisible-code-block: python
%
% # assert that the result is 'en'
% self.assertEqual(lang, 'en')

(portal-get-current-language-example)=

## Get current language

To get the currently negotiated language, use {meth}`api.portal.get_current_language`.

```python
from plone import api
lang = api.portal.get_current_language()
```

% invisible-code-block: python
%
% # assert that the result is 'en'
% self.assertEqual(lang, 'en')

(portal-translate-example)=

## Translate

To translate a message in a given language, use {meth}`api.portal.translate`.

```python
from plone import api
msg = api.portal.translate('Edited', lang='es')
```

% invisible-code-block: python
%
% # assert that the translation is correct
% self.assertEqual(msg, 'Editado')

(portal-send-email-example)=

## Send E-Mail

To send an e-mail use {meth}`api.portal.send_email`:

% invisible-code-block: python
%
% # Mock the mail host so we can test sending the email
% from plone import api
% from Products.CMFPlone.tests.utils import MockMailHost
% from Products.CMFPlone.utils import getToolByName
% from Products.MailHost.interfaces import IMailHost
% api.portal.PRINTINGMAILHOST_ENABLED = True
%
% mockmailhost = MockMailHost('MailHost')
% if not hasattr(mockmailhost, 'smtp_host'):
%     mockmailhost.smtp_host = 'localhost'
% portal = api.portal.get()
% portal.MailHost = mockmailhost
% sm = portal.getSiteManager()
% sm.registerUtility(component=mockmailhost, provided=IMailHost)
% mailhost = getToolByName(portal, 'MailHost')
% mailhost.reset()

```python
from plone import api
api.portal.send_email(
    recipient="bob@plone.org",
    sender="noreply@plone.org",
    subject="Trappist",
    body="One for you Bob!",
)
```

% invisible-code-block: python
%
% self.assertEqual(len(mailhost.messages), 1)
%
% try:
%     # Python 3
%     from email import message_from_bytes
% except ImportError:
%     # Python 2
%     from email import message_from_string as message_from_bytes
% msg = message_from_bytes(mailhost.messages[0])
% self.assertEqual(msg['To'], 'bob@plone.org')
% self.assertEqual(msg['From'], 'noreply@plone.org')
% self.assertEqual(msg['Subject'], '=?utf-8?q?Trappist?=')
% self.assertEqual(msg.get_payload(), 'One for you Bob!')

If you need to add other fields not supported on send_email signature,
Python's standard [email module](https://docs.python.org/2.7/library/email.message.html#email.message.Message) can also be used:

```python
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
```

% invisible-code-block: python
%
% self.assertEqual(len(mailhost.messages), 2)
%
% msg = message_from_bytes(mailhost.messages[1])
% payloads = msg.get_payload()
% self.assertEqual(len(payloads), 2)
% self.assertEqual(msg['Reply-To'], 'community@plone.org')
% self.assertEqual(payloads[0].get_payload(), 'One for you Bar!')
% self.assertIn(
%     'attachment; filename="report.xml',
%     payloads[1]['Content-Disposition']
% )
% api.portal.PRINTINGMAILHOST_ENABLED = False
% mailhost.reset()

(portal-show-message-example)=

## Show notification message

With {meth}`api.portal.show_message` you can show a notification message to the user.

```python
from plone import api
api.portal.show_message(message='Blueberries!', request=request)
```

% invisible-code-block: python
%
% from Products.statusmessages.interfaces import IStatusMessage
% messages = IStatusMessage(request)
% show = messages.show()
% self.assertEqual(len(show), 1)
% self.assertTrue('Blueberries!' in show[0].message)

Since version `2.0.0`, the `request` argument can be omitted.
In that case, the global request will be used.

```python
api.portal.show_message(message='Cranberries!')
```

% invisible-code-block: python
%
% from Products.statusmessages.interfaces import IStatusMessage
% messages = IStatusMessage(request)
% show = messages.show()
% self.assertTrue('Cranberries!' in show[-1].message)

(portal-get-registry-record-example)=

## Get plone.app.registry record

Plone comes with a package `plone.app.registry` that provides a common way to store configuration and settings.
{meth}`api.portal.get_registry_record` provides an easy way to access these.

% invisible-code-block: python
%
% from plone.registry.interfaces import IRegistry
% from plone.registry.record import Record
% from plone.registry import field
% from zope.component import getUtility
% registry = getUtility(IRegistry)
% registry.records['my.package.someoption'] = Record(field.Bool(
%         title=u"Foo"))
% registry['my.package.someoption'] = True

```python
from plone import api
api.portal.get_registry_record('my.package.someoption')
```

% invisible-code-block: python
%
% self.assertTrue(api.portal.get_registry_record('my.package.someoption'))

One common pattern when using registry records is to define an interface with all the settings.
{meth}`api.portal.get_registry_record` also allows you to use this pattern.

% invisible-code-block: python
%
% from plone.registry.interfaces import IRegistry
% from plone.api.tests.test_portal import IMyRegistrySettings
%
% registry = getUtility(IRegistry)
% registry.registerInterface(IMyRegistrySettings)
% records = registry.forInterface(IMyRegistrySettings)
% records.field_one = 'my text'

```python
from plone import api
api.portal.get_registry_record('field_one', interface=IMyRegistrySettings)
```

% invisible-code-block: python
%
% self.assertEqual(
%     api.portal.get_registry_record('field_one', interface=IMyRegistrySettings),
%     'my text'
% )

It is possible to provide a default value that will be returned by {meth}`api.portal.get_registry_record`, if the queried record is not found.

```python
from plone import api
api.portal.get_registry_record('foo', interface=IMyRegistrySettings, default='bar')
api.portal.get_registry_record('foo', default='baz')
```

% invisible-code-block: python
% self.assertEqual(
%     api.portal.get_registry_record(
%         'foo',
%         interface=IMyRegistrySettings,
%         default='bar'
%     ),
%     'bar',
% )
% self.assertEqual(
%     api.portal.get_registry_record('foo', default='baz'),
%     'baz',
% )

(portal-set-registry-record-example)=

## Set plone.app.registry record

{meth}`api.portal.set_registry_record` provides an easy way to change `plone.app.registry` configuration and settings.

% invisible-code-block: python
%
% from plone.registry.interfaces import IRegistry
% from plone.registry.record import Record
% from plone.registry import field
% from zope.component import getUtility
% registry = getUtility(IRegistry)
% registry.records['my.package.someoption'] = Record(field.Bool(
%         title=u"Foo"))
% registry['my.package.someoption'] = True

```python
from plone import api
api.portal.set_registry_record('my.package.someoption', False)
```

% invisible-code-block: python
%
% self.assertFalse(registry['my.package.someoption'])

{meth}`api.portal.set_registry_record` allows you to define an interface with all the settings.

% invisible-code-block: python
%
% from plone.registry.interfaces import IRegistry
% from plone.api.tests.test_portal import IMyRegistrySettings
%
% registry = getUtility(IRegistry)
% registry.registerInterface(IMyRegistrySettings)
% records = registry.forInterface(IMyRegistrySettings)

```python
from plone import api
api.portal.set_registry_record('field_one', 'new value', interface=IMyRegistrySettings)
```

% invisible-code-block: python
%
% self.assertEqual(
%     api.portal.get_registry_record('field_one', interface=IMyRegistrySettings),
%     'new value'
% )

(portal-get-vocabulary-example)=

## Get vocabulary

To get a vocabulary by name, use {func}`api.portal.get_vocabulary`.

```python
from plone import api

# Get vocabulary using default portal context
vocabulary = api.portal.get_vocabulary(name='plone.app.vocabularies.PortalTypes')

# Get vocabulary with specific context
context = api.portal.get()
states_vocabulary = api.portal.get_vocabulary(
    name='plone.app.vocabularies.WorkflowStates',
    context=context
)
```

(portal-get-all-vocabulary-names-example)=

## Get all vocabulary names

To get a list of all available vocabulary names in your Plone site, use {meth}`api.portal.get_vocabulary_names`.

```python
from plone import api

# Get all vocabulary names
vocabulary_names = api.portal.get_vocabulary_names()

# Common vocabularies that should be available
common_vocabularies = [
    'plone.app.vocabularies.PortalTypes',
    'plone.app.vocabularies.WorkflowStates',
    'plone.app.vocabularies.WorkflowTransitions'
]

for vocabulary_name in common_vocabularies:
    assert vocabulary_name in vocabulary_names
```

## Further reading

For more information on possible flags and usage options please see the full {ref}`plone-api-portal` specification.
