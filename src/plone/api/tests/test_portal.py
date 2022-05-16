"""Tests for plone.api.portal."""

from datetime import date
from datetime import datetime
from pkg_resources import parse_version
from plone.api import content
from plone.api import env
from plone.api import portal
from plone.api.tests.base import INTEGRATION_TESTING
from plone.app.layout.navigation.interfaces import INavigationRoot
from plone.registry import field
from plone.registry.interfaces import IRegistry
from plone.registry.record import Record
from Products.CMFCore.utils import getToolByName
from Products.CMFPlone.tests.utils import MockMailHost
from Products.MailHost.interfaces import IMailHost
from unittest import mock
from zope import schema
from zope.component import getUtility
from zope.component.hooks import setSite
from zope.interface import Interface
from zope.site import LocalSiteManager

import DateTime
import unittest


try:
    # Python 3
    from email import message_from_bytes
except ImportError:
    # Python 2
    from email import message_from_string as message_from_bytes


HAS_PLONE5 = parse_version(env.plone_version()) >= parse_version("5.0b2")


class IMyRegistrySettings(Interface):

    field_one = schema.TextLine(
        title="something",
        description="something else",
    )

    field_two = schema.TextLine(
        title="something",
        description="something else",
    )


class IMyOtherRegistrySettings(Interface):

    field_three = schema.TextLine(
        title="something",
        description="something else",
    )


class ImNotAnInterface:
    pass


class TestPloneApiPortal(unittest.TestCase):
    """Unit tests for getting portal info using plone.api."""

    layer = INTEGRATION_TESTING

    def setUp(self):
        """Shared test environment set-up, ran before every test."""
        self.portal = self.layer["portal"]

        # Mock the mail host so we can test sending the email
        mockmailhost = MockMailHost("MailHost")

        if not getattr(mockmailhost, "smtp_host", None):
            mockmailhost.smtp_host = "localhost"

        self.portal.MailHost = mockmailhost
        sm = self.portal.getSiteManager()
        sm.registerUtility(component=mockmailhost, provided=IMailHost)

        self.mailhost = portal.get_tool("MailHost")
        if HAS_PLONE5:
            portal.set_registry_record(
                "plone.email_from_name",
                "Portal Owner",
            )
            portal.set_registry_record(
                "plone.email_from_address",
                "sender@example.org",
            )
        else:
            self.portal._updateProperty(
                "email_from_name",
                "Portal Owner",
            )
            self.portal._updateProperty(
                "email_from_address",
                "sender@example.org",
            )

    def _set_localization_date_format(self):
        """Set the expected localized date format."""
        from plone.api.exc import InvalidParameterError

        name_root = "Products.CMFPlone.i18nl10n.override_dateformat."
        try:
            portal.set_registry_record(
                name=name_root + "Enabled",
                value=True,
            )
            portal.set_registry_record(
                name=name_root + "date_format_long",
                value="%b %d, %Y %I:%M %p",
            )
            portal.set_registry_record(
                name=name_root + "time_format",
                value="%I:%M %p",
            )
            portal.set_registry_record(
                name=name_root + "date_format_short",
                value="%b %d, %Y",
            )
        except InvalidParameterError:
            # before Plone 4.3, date formats were stored in portal_properties
            properties = portal.get_tool("portal_properties")
            properties.localLongTimeFormat = "%b %d, %Y %I:%M %p"
            properties.localTimeOnlyFormat = "%I:%M %p"
            properties.localTimeFormat = "%b %d, %Y"

    def test_get(self):
        """Test getting the portal object."""
        self.assertEqual(portal.get(), self.portal)

    def test_get_with_sub_site(self):
        """Using getSite() alone is not enough to get the portal. It
        will return the closest site, which may return a sub site
        instead of the portal.

        Set a different local site manager and test that portal.get()
        still returns the portal.
        """
        a_site = content.create(
            container=self.portal,
            type="Folder",
            title="A Site",
        )
        a_site.setSiteManager(LocalSiteManager(a_site))

        setSite(a_site)

        self.assertEqual(portal.get(), self.portal)

        # cleanup
        setSite(self.portal)

    @mock.patch("plone.api.portal.getSite")
    def test_get_no_site(self, getSite):
        """Test error msg when getSite() returns None."""
        getSite.return_value = None
        from plone.api.exc import CannotGetPortalError

        with self.assertRaises(CannotGetPortalError):
            portal.get()

    def test_get_tool_constraints(self):
        """Test the constraints for getting a tool."""

        # When no parameters are given an error is raised
        from plone.api.exc import MissingParameterError

        with self.assertRaises(MissingParameterError):
            portal.get_tool()

    def test_get_tool_tool_not_found(self):
        """Test that error msg lists available tools if a tool is not found."""
        from plone.api.exc import InvalidParameterError

        with self.assertRaises(InvalidParameterError) as cm:
            portal.get_tool("portal_foo")

        self.assertTrue(
            str(cm.exception).startswith(
                "Cannot find a tool with name 'portal_foo'",
            ),
        )

        # A selection of portal tools which should exist in all plone versions
        should_be_theres = (
            "portal_setup",
            "portal_catalog",
        )

        for should_be_there in should_be_theres:
            self.assertIn((should_be_there + "\n"), str(cm.exception))

    def test_get_tool(self):
        """Test to validate the tool name."""

        self.assertEqual(
            portal.get_tool(name="portal_catalog"),
            getToolByName(self.portal, "portal_catalog"),
        )
        self.assertEqual(
            portal.get_tool(name="portal_membership"),
            getToolByName(self.portal, "portal_membership"),
        )

    def test_send_email_constraints(self):
        """Test the constraints for sending an email."""
        from plone.api.exc import MissingParameterError

        # When no parameters are given an error is raised
        with self.assertRaises(MissingParameterError):
            portal.send_email()

        # recipient, subject and body are required
        with self.assertRaises(MissingParameterError):
            portal.send_email(
                subject="Beer",
                body="To beer or not to beer, that is the question",
            )
        with self.assertRaises(MissingParameterError):
            portal.send_email(
                recipient="joe@example.org",
                subject="Beer",
            )
        with self.assertRaises(MissingParameterError):
            portal.send_email(
                recipient="joe@example.org",
                body="To beer or not to beer, that is the question",
            )

    def test_send_email(self):
        """Test sending mail."""

        self.mailhost.reset()

        portal.send_email(
            recipient="bob@plone.org",
            sender="noreply@plone.org",
            subject="Trappist",
            body="One for you Bob!",
        )

        self.assertEqual(len(self.mailhost.messages), 1)
        msg = message_from_bytes(self.mailhost.messages[0])
        self.assertEqual(msg["To"], "bob@plone.org")
        self.assertEqual(msg["From"], "noreply@plone.org")
        self.assertEqual(msg["Subject"], "=?utf-8?q?Trappist?=")
        self.assertEqual(msg.get_payload(), "One for you Bob!")
        self.mailhost.reset()

        # When no sender is set, we take the portal properties.
        portal.send_email(
            recipient="bob@plone.org",
            subject="Trappist",
            body="One for you Bob!",
        )

        self.assertEqual(len(self.mailhost.messages), 1)
        msg = message_from_bytes(self.mailhost.messages[0])
        self.assertEqual(msg["From"], "Portal Owner <sender@example.org>")

    def test_send_email_without_configured_mailhost(self):
        """By default, the MailHost is not configured yet, so we cannot
        send email.
        """
        if HAS_PLONE5:
            old_value = portal.get_registry_record("plone.email_from_address")
            portal.set_registry_record("plone.email_from_address", "")  # ASCII
        else:
            old_smtp_host = self.portal.MailHost.smtp_host
            self.portal.MailHost.smtp_host = None

        with self.assertRaises(ValueError):
            portal.send_email(
                recipient="bob@plone.org",
                sender="noreply@plone.org",
                subject="Trappist",
                body="One for you Bob!",
            )

        if HAS_PLONE5:
            portal.set_registry_record("plone.email_from_address", old_value)
        else:
            self.portal.MailHost.smtp_host = old_smtp_host

    @mock.patch("plone.api.portal.parseaddr")
    def test_send_email_parseaddr(self, mock_parseaddr):
        """Simulate faulty parsing in parseaddr, from_address should be
        default email_from_address.
        """

        self.mailhost.reset()

        mock_parseaddr.return_value = ("Chuck Norris", "chuck@norris.org")
        portal.send_email(
            recipient="bob@plone.org",
            subject="Trappist",
            body="One for you Bob!",
        )

    def test_send_email_with_config_in_registry(self):
        """Test mail-setting being stored in registry"""
        self.mailhost.reset()

        portal.set_registry_record(
            "plone.email_from_address",
            "reg@example.org",
        )  # ASCII
        portal.set_registry_record(
            "plone.email_from_name",
            "Registry",
        )  # TextLine
        portal.send_email(
            recipient="bob@plone.org",
            subject="Trappist",
            body="One for you Bob!",
        )
        self.assertEqual(len(self.mailhost.messages), 1)
        msg = message_from_bytes(self.mailhost.messages[0])
        self.assertEqual(msg["From"], "Registry <reg@example.org>")

    def test_send_email_with_printingmailhost(self):
        """Test that send_email does not raise an exception when
        Products.PrintingMailHost is installed and active.
        """
        old_flag = portal.PRINTINGMAILHOST_ENABLED

        if HAS_PLONE5:
            old_value = portal.get_registry_record("plone.email_from_address")
            portal.set_registry_record("plone.email_from_address", "")  # ASCII
        else:
            old_smtp_host = self.portal.MailHost.smtp_host
            self.portal.MailHost.smtp_host = None

        # PrintingMailHost disabled
        portal.PRINTINGMAILHOST_ENABLED = False
        with self.assertRaises(ValueError):
            portal.send_email(
                recipient="bob@plone.org",
                sender="noreply@plone.org",
                subject="Trappist",
                body="One for you Bob!",
            )

        # PrintingMailHost enabled
        portal.PRINTINGMAILHOST_ENABLED = True
        portal.send_email(
            recipient="bob@plone.org",
            sender="noreply@plone.org",
            subject="Trappist",
            body="One for you Bob!",
        )

        # Prevents sideeffects in other tests.
        if HAS_PLONE5:
            portal.set_registry_record("plone.email_from_address", old_value)
        else:
            self.portal.MailHost.smtp_host = old_smtp_host
        portal.PRINTINGMAILHOST_ENABLED = old_flag

    def test_get_localized_time_constraints(self):
        """Test the constraints for get_localized_time."""

        # When no parameters are given an error is raised
        from plone.api.exc import MissingParameterError

        with self.assertRaises(MissingParameterError):
            portal.get_localized_time()

    def test_get_localized_time(self):
        """Test getting the localized time."""

        # set the expected localized date format
        self._set_localization_date_format()

        # tests
        result = portal.get_localized_time(
            datetime=DateTime.DateTime(1999, 12, 31, 23, 59),
            long_format=True,
        )
        self.assertEqual(result, "Dec 31, 1999 11:59 PM")

        result = portal.get_localized_time(
            datetime=DateTime.DateTime(1999, 12, 31, 23, 59),
            time_only=True,
        )
        self.assertEqual(result, "11:59 PM")

        result = portal.get_localized_time(
            datetime=DateTime.DateTime(1999, 12, 31, 23, 59),
        )
        self.assertEqual(result, "Dec 31, 1999")

    def test_get_localized_time_python_datetime(self):
        """Test getting the localized time using Python datetime.datetime."""

        # set the expected localized date format
        self._set_localization_date_format()

        # tests
        result = portal.get_localized_time(
            datetime=datetime(1999, 12, 31, 23, 59),
            long_format=True,
        )
        self.assertEqual(result, "Dec 31, 1999 11:59 PM")

        result = portal.get_localized_time(
            datetime=datetime(1999, 12, 31, 23, 59),
            time_only=True,
        )
        self.assertEqual(result, "11:59 PM")

        result = portal.get_localized_time(
            datetime=datetime(1999, 12, 31, 23, 59),
        )
        self.assertEqual(result, "Dec 31, 1999")

    def test_get_localized_time_python_date(self):
        """Test getting the localized time using Python datetime.date."""

        # set the expected localized date format
        self._set_localization_date_format()

        # tests
        result = portal.get_localized_time(
            datetime=date(1999, 12, 31),
            long_format=True,
        )
        self.assertEqual(result, "Dec 31, 1999")

        result = portal.get_localized_time(
            datetime=date(1999, 12, 31),
            time_only=True,
        )
        self.assertEqual(result, "")

        result = portal.get_localized_time(
            datetime=date(1999, 12, 31),
        )
        self.assertEqual(result, "Dec 31, 1999")

    def test_show_message_constraints(self):
        """Test the constraints for show_message."""
        from plone.api.exc import MissingParameterError

        # When no parameters are given an error is raised
        with self.assertRaises(MissingParameterError):
            portal.show_message()

        # message is a required parameter
        with self.assertRaises(MissingParameterError):
            portal.show_message(request=self.layer["request"])

    def test_show_message(self):
        """Test to see if message appears."""

        from Products.statusmessages.interfaces import IStatusMessage

        request = self.layer["request"]
        portal.show_message(message="Blueberries!", request=request)
        messages = IStatusMessage(request)
        show = messages.show()
        self.assertEqual(len(show), 1)
        self.assertIn("Blueberries!", show[0].message)
        portal.show_message(message="One", request=request)
        portal.show_message(message="Two", request=request)
        messages = IStatusMessage(request)
        show = messages.show()
        self.assertEqual(len(show), 2)
        self.assertEqual(show[0].message, "One")
        self.assertEqual(show[1].message, "Two")

    def test_get_navigation_root(self):
        """Test to see if the navigation_root is returned."""

        navigation_root = portal.get_navigation_root(portal.get())
        self.assertTrue(INavigationRoot.providedBy(navigation_root))

        from plone.api.exc import MissingParameterError

        with self.assertRaises(MissingParameterError):
            portal.get_navigation_root()

    def test_get_existing_registry_record(self):
        """Test that existing registry records are returned correctly."""
        registry = getUtility(IRegistry)
        registry.records["plone.api.norris_power"] = Record(
            field.TextLine(title="Chuck Norris' Power"),
        )
        registry.records["plone.api.unset"] = Record(
            field.TextLine(title="An unset field"),
        )
        registry["plone.api.norris_power"] = "infinite"

        self.assertEqual(
            portal.get_registry_record("plone.api.norris_power"),
            "infinite",
        )

        self.assertEqual(
            portal.get_registry_record("plone.api.unset"),
            None,
        )

    def test_get_missing_registry_record(self):
        """Test that getting a missing registry record raises an Exception."""
        from plone.api.exc import MissingParameterError

        with self.assertRaises(MissingParameterError):
            portal.get_registry_record()

    def test_get_invalid_registry_record(self):
        """Test that getting an invalid registry record raises an Exception."""
        from plone.api.exc import InvalidParameterError

        with self.assertRaises(InvalidParameterError):
            portal.get_registry_record(name=dict({"foo": "bar"}))

    def test_get_invalid_registry_record_msg(self):
        """Test that the error message from trying to get a
        nonexistant registry record produces an error message which
        lists suggested registry records.
        """
        from plone.api.exc import InvalidParameterError

        with self.assertRaises(InvalidParameterError) as cm:
            portal.get_registry_record(name="nonexistent.sharepoint.power")
        exc_str = str(cm.exception)

        # Check if there is an error message.
        self.assertTrue(exc_str.startswith("Cannot find a record with name"))

    def test_get_invalid_registry_record_suggestions(self):
        from plone.api.exc import InvalidParameterError

        # Check without suggestion
        with self.assertRaises(InvalidParameterError) as cm:
            portal.get_registry_record(name="a random unique string")
        exc_str = str(cm.exception)

        # Check for an error, but no suggestions.
        self.assertTrue(exc_str.startswith("Cannot find a record with name"))
        self.assertFalse("Did you mean?:" in exc_str)

        # Check with suggestions
        with self.assertRaises(InvalidParameterError) as cm:
            portal.get_registry_record(name="querystring")
        exc_str = str(cm.exception)

        # Check for an error with suggestions.
        self.assertTrue(exc_str.startswith("Cannot find a record with name"))
        self.assertTrue("Did you mean?:" in exc_str)

    def test_get_registry_record_from_interface(self):
        """Test that getting a record from an interface works."""
        registry = getUtility(IRegistry)
        registry.registerInterface(IMyRegistrySettings)

        self.assertEqual(
            portal.get_registry_record(
                "field_one",
                interface=IMyRegistrySettings,
            ),
            None,
        )

    def test_get_invalid_interface_for_registry_record(self):
        """Test that passing an invalid interface raises an Exception."""
        from plone.api.exc import InvalidParameterError

        with self.assertRaises(InvalidParameterError):
            portal.get_registry_record(
                "something",
                interface=ImNotAnInterface,
            )

    def test_get_invalid_interface_for_registry_record_msg(self):
        """Test that a helpful message is shown when passing an invalid
        interface.
        """
        from plone.api.exc import InvalidParameterError

        with self.assertRaises(InvalidParameterError) as cm:
            portal.get_registry_record(
                "something",
                interface=ImNotAnInterface,
            )
        exc_str = str(cm.exception)

        # Check if there is an error message.
        self.assertTrue(exc_str.startswith("The interface parameter has to "))

    def test_get_invalid_record_in_interface_for_registry_record(self):
        """Test that trying to get an invalid field from an interface raises
        an Exception.
        """
        from plone.api.exc import InvalidParameterError

        registry = getUtility(IRegistry)
        registry.registerInterface(IMyRegistrySettings)

        with self.assertRaises(InvalidParameterError):
            portal.get_registry_record(
                "non_existing_field",
                interface=IMyRegistrySettings,
            )

    def test_get_invalid_record_in_interface_for_registry_record_msg(self):
        """Test that a helpful message is shown when trying to get an invalid
        field from an interface.
        """
        from plone.api.exc import InvalidParameterError

        registry = getUtility(IRegistry)
        registry.registerInterface(IMyRegistrySettings)

        with self.assertRaises(InvalidParameterError) as cm:
            portal.get_registry_record(
                "non_existing_field",
                interface=IMyRegistrySettings,
            )
        exc_str = str(cm.exception)

        # Check if there is an error message.
        self.assertTrue(exc_str.startswith("Cannot find a record with name "))
        self.assertTrue(exc_str.find(" on interface ") != -1)
        self.assertTrue(exc_str.find("field_one") != -1)
        self.assertTrue(exc_str.find("field_two") != -1)

    def test_get_invalid_record_with_default(self):
        """If get_registry_record is called with a default parameter
        and the record cannot be resolved
        the default will be returned instead of raising InvalidParameterError
        """
        registry = getUtility(IRegistry)
        registry.registerInterface(IMyRegistrySettings)

        self.assertEqual(
            portal.get_registry_record(
                "non_existing_field",
                interface=IMyRegistrySettings,
                default=1,
            ),
            1,
        )
        self.assertEqual(
            portal.get_registry_record(
                "something",
                default=2,
            ),
            2,
        )

    def test_set_valid_registry_record(self):
        """Test that setting a valid registry record succeeds."""
        registry = getUtility(IRegistry)
        registry.records["plone.api.plone_power"] = Record(
            field.TextLine(title="Plone's Power"),
        )
        portal.set_registry_record("plone.api.plone_power", "awesome")
        self.assertEqual(registry["plone.api.plone_power"], "awesome")

    def test_set_missing_param_registry_record(self):
        """Test that when set_registry_record is called without
        parameters, a MissingParameterError exception is raised.
        """
        from plone.api.exc import MissingParameterError

        with self.assertRaises(MissingParameterError):
            portal.set_registry_record()

    def test_set_non_existing_record_value(self):
        """Test that setting the value of a non existent record raises
        an Exception.
        """
        from plone.api.exc import InvalidParameterError

        with self.assertRaises(InvalidParameterError):
            portal.set_registry_record(
                name="nonexistent.sharepoint.power",
                value="Zero",
            )

    def test_set_no_value_param_for_existing_record(self):
        """Test that calling portal.set_registry_record with a name
        parameter for an existing record, but without a value, raises
        an Exception.
        """
        registry = getUtility(IRegistry)
        registry.records["plone.api.plone_power"] = Record(
            field.TextLine(title="Plone's Power"),
        )

        from plone.api.exc import MissingParameterError

        with self.assertRaises(MissingParameterError):
            portal.set_registry_record(name="plone.api.plone_power")

    def test_set_invalid_key_type_record(self):
        """Test that trying to set the value of a record by passing a
        list for the record name instead of a string, raises an error.
        """
        from plone.api.exc import InvalidParameterError

        with self.assertRaises(InvalidParameterError):
            portal.set_registry_record(
                name=["foo", "bar"],
                value="baz",
            )

    def test_set_registry_record_from_interface(self):
        """Test that setting a value on a record from an interface works."""
        registry = getUtility(IRegistry)
        registry.registerInterface(IMyRegistrySettings)

        text = "random text"
        portal.set_registry_record(
            "field_one",
            text,
            interface=IMyRegistrySettings,
        )
        self.assertEqual(
            portal.get_registry_record(
                "field_one",
                interface=IMyRegistrySettings,
            ),
            text,
        )

    def test_set_registry_record_with_invalid_value(self):
        """Test setting an invalid value on a record from an interface.

        This should give an invalid parameter error.
        See also https://github.com/plone/plone.api/issues/435
        and duplicate: https://github.com/plone/plone.api/issues/464
        """
        from plone.api.exc import InvalidParameterError

        registry = getUtility(IRegistry)
        registry.registerInterface(IMyOtherRegistrySettings)
        with self.assertRaises(InvalidParameterError) as cm:
            portal.set_registry_record(
                "field_three",
                42,
                interface=IMyOtherRegistrySettings,
            )
        exc_str = str(cm.exception)

        self.assertIn("The value parameter for the field field_three", exc_str)
        self.assertIn("TextLine", exc_str)

    def test_set_registry_record_on_invalid_interface(self):
        """Test that passing an invalid interface raises an Exception."""
        from plone.api.exc import InvalidParameterError

        with self.assertRaises(InvalidParameterError):
            portal.set_registry_record(
                "something",
                "value",
                interface=ImNotAnInterface,
            )

    def test_set_registry_record_on_invalid_interface_msg(self):
        """Test that a helpful message is shown when passing an invalid
        interface.
        """
        from plone.api.exc import InvalidParameterError

        with self.assertRaises(InvalidParameterError) as cm:
            portal.set_registry_record(
                "something",
                "value",
                interface=ImNotAnInterface,
            )
        exc_str = str(cm.exception)

        # Check if there is an error message.
        self.assertTrue(exc_str.startswith("The interface parameter has to "))

    def test_set_invalid_registry_record_from_interface(self):
        """Test that trying to set an invalid field from an interface raises
        an Exception.
        """
        from plone.api.exc import InvalidParameterError

        registry = getUtility(IRegistry)
        registry.registerInterface(IMyRegistrySettings)

        with self.assertRaises(InvalidParameterError):
            portal.set_registry_record(
                "non_existing_field",
                "value",
                interface=IMyRegistrySettings,
            )

    def test_set_invalid_registry_record_from_interface_msg(self):
        """Test that a helpful message is shown when trying to set an invalid
        field from an interface.
        """
        from plone.api.exc import InvalidParameterError

        registry = getUtility(IRegistry)
        registry.registerInterface(IMyRegistrySettings)

        with self.assertRaises(InvalidParameterError) as cm:
            portal.set_registry_record(
                "non_existing_field",
                "value",
                interface=IMyRegistrySettings,
            )
        exc_str = str(cm.exception)

        # Check if there is an error message.
        self.assertTrue(exc_str.startswith("Cannot find a record with name "))
        self.assertTrue(exc_str.find(" on interface ") != -1)
        self.assertTrue(exc_str.find("field_one") != -1)
        self.assertTrue(exc_str.find("field_two") != -1)

    def test_set_invalid_value_on_registry_record_from_interface(self):
        """Test that setting a value not meant for the record raises an
        Exception..
        """
        from plone.api.exc import InvalidParameterError

        registry = getUtility(IRegistry)
        registry.registerInterface(IMyRegistrySettings)

        with self.assertRaises(InvalidParameterError):
            portal.set_registry_record(
                "field_one",
                b"value",
                interface=IMyRegistrySettings,
            )

    def test_set_invalid_value_on_registry_record_from_interface_msg(self):
        """Test that setting a value not meant for the record raises an
        Exception..
        """
        from plone.api.exc import InvalidParameterError

        registry = getUtility(IRegistry)
        registry.registerInterface(IMyRegistrySettings)

        with self.assertRaises(InvalidParameterError) as cm:
            portal.set_registry_record(
                "field_one",
                b"value",
                interface=IMyRegistrySettings,
            )
        exc_str = str(cm.exception)

        # Check if there is an error message.
        self.assertTrue(
            exc_str.startswith("The value parameter for the field"),
        )
        self.assertTrue(exc_str.find(" needs to be ") != -1)
        self.assertTrue(exc_str.find("TextLine") != -1)

    def test_get_default_language(self):
        """Test that default language is properly returned."""
        self.assertEqual(portal.get_default_language(), "en")

    def test_get_current_language(self):
        """Test that current language is properly returned."""
        self.assertEqual(portal.get_current_language(portal.get()), "en")
        self.layer["request"]["LANGUAGE"] = "fr"
        self.assertEqual(portal.get_current_language(), "fr")

    def test_translate(self):
        """Test translation."""
        self.assertEqual(
            portal.translate(
                "A workflow action triggers a workflow transition on an " "object.",
                lang="es",
            ),
            "Una acción de flujo de trabajo dispara una transición de "
            "flujo de trabajo en un objeto.",
        )
        self.assertEqual(
            portal.translate(
                "month_apr",
                domain="plonelocales",
                lang="fr",
            ),
            "Avril",
        )
