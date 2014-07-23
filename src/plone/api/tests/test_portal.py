# -*- coding: utf-8 -*-
"""Tests for plone.api.portal."""

from DateTime import DateTime
from Products.CMFCore.utils import getToolByName
from Products.CMFPlone.tests.utils import MockMailHost
from Products.MailHost.interfaces import IMailHost
from datetime import date
from datetime import datetime
from email import message_from_string
from plone.api import content
from plone.api import portal
from plone.api.tests.base import INTEGRATION_TESTING
from plone.app.layout.navigation.interfaces import INavigationRoot
from plone.registry import field
from plone.registry.interfaces import IRegistry
from plone.registry.record import Record
from zope.component import getUtility
from zope.component.hooks import setSite
from zope.site import LocalSiteManager

import mock
import unittest2 as unittest


class TestPloneApiPortal(unittest.TestCase):
    """Unit tests for getting portal info using plone.api."""

    layer = INTEGRATION_TESTING

    def setUp(self):
        """Shared test environment set-up, ran before every test."""
        self.portal = self.layer['portal']

        # Mock the mail host so we can test sending the email
        mockmailhost = MockMailHost('MailHost')

        if not hasattr(mockmailhost, 'smtp_host'):
            mockmailhost.smtp_host = 'localhost'

        self.portal.MailHost = mockmailhost
        sm = self.portal.getSiteManager()
        sm.registerUtility(component=mockmailhost, provided=IMailHost)

        self.mailhost = portal.get_tool('MailHost')

        self.portal._updateProperty('email_from_name', 'Portal Owner')
        self.portal._updateProperty('email_from_address', 'sender@example.org')

    def _set_localization_date_format(self):
        """Set the expected localized date format."""
        from plone.api.exc import InvalidParameterError

        name_root = 'Products.CMFPlone.i18nl10n.override_dateformat.'
        try:
            portal.set_registry_record(
                name=name_root + 'Enabled',
                value=True,
            )
            portal.set_registry_record(
                name=name_root + 'date_format_long',
                value='%b %d, %Y %I:%M %p',
            )
            portal.set_registry_record(
                name=name_root + 'time_format',
                value='%I:%M %p',
            )
            portal.set_registry_record(
                name=name_root + 'date_format_short',
                value='%b %d, %Y',
            )
        except InvalidParameterError:
            # before Plone 4.3, date formats were stored in portal_properties
            properties = portal.get_tool('portal_properties')
            properties.localLongTimeFormat = '%b %d, %Y %I:%M %p'
            properties.localTimeOnlyFormat = '%I:%M %p'
            properties.localTimeFormat = '%b %d, %Y'

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
            container=self.portal, type="Folder", title="A Site")
        a_site.setSiteManager(LocalSiteManager(a_site))

        setSite(a_site)

        self.assertEqual(portal.get(), self.portal)

        # cleanup
        setSite(self.portal)

    @mock.patch('plone.api.portal.getSite')
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
            portal.get_tool('portal_foo')

        self.assertTrue(
            str(cm.exception).startswith(
                "Cannot find a tool with name 'portal_foo'"))

        # A selection of portal tools which should exist in all plone versions
        should_be_theres = (
            "portal_setup",
            "portal_actionicons",
            "portal_actions",
            "portal_atct",
            "portal_calendar",
            "portal_catalog",
            "portal_controlpanel",
            "portal_css",
            "portal_diff",
            "portal_factory",
            "portal_groupdata",
            "portal_groups",
            "portal_interface",
            "portal_javascripts",
            "portal_memberdata",
            "portal_membership",
            "portal_metadata",
            "portal_migration",
            "portal_password_reset",
            "portal_properties",
            "portal_quickinstaller",
            "portal_registration",
            "portal_skins",
            "portal_types",
            "portal_uidannotation",
            "portal_uidgenerator",
            "portal_uidhandler",
            "portal_undo",
            "portal_url",
            "portal_view_customizations",
            "portal_workflow",
        )

        for should_be_there in should_be_theres:
            self.assertIn((should_be_there + '\n'), str(cm.exception))

    def test_get_tool(self):
        """Test to validate the tool name."""

        self.assertEqual(
            portal.get_tool(name='portal_catalog'),
            getToolByName(self.portal, 'portal_catalog'),
        )
        self.assertEqual(
            portal.get_tool(name='portal_membership'),
            getToolByName(self.portal, 'portal_membership'),
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
                subject='Beer',
                body="To beer or not to beer, that is the question",
            )
        with self.assertRaises(MissingParameterError):
            portal.send_email(
                recipient='joe@example.org',
                subject='Beer',
            )
        with self.assertRaises(MissingParameterError):
            portal.send_email(
                recipient='joe@example.org',
                body="To beer or not to beer, that is the question",
            )

    def test_send_email(self):
        """Test sending mail."""

        self.mailhost.reset()

        portal.send_email(
            recipient="bob@plone.org",
            sender="noreply@plone.org",
            subject="Trappist",
            body=u"One for you Bob!",
        )

        self.assertEqual(len(self.mailhost.messages), 1)
        msg = message_from_string(self.mailhost.messages[0])
        self.assertEqual(msg['To'], 'bob@plone.org')
        self.assertEqual(msg['From'], 'noreply@plone.org')
        self.assertEqual(msg['Subject'], '=?utf-8?q?Trappist?=')
        self.assertEqual(msg.get_payload(), u'One for you Bob!')
        self.mailhost.reset()

        # When no sender is set, we take the portal properties.
        portal.send_email(
            recipient="bob@plone.org",
            subject="Trappist",
            body=u"One for you Bob!",
        )

        self.assertEqual(len(self.mailhost.messages), 1)
        msg = message_from_string(self.mailhost.messages[0])
        self.assertEqual(msg['From'], 'Portal Owner <sender@example.org>')

    def test_send_email_without_configured_mailhost(self):
        """By default, the MailHost is not configured yet, so we cannot
        send email.
        """
        self.portal._updateProperty('email_from_address', None)
        with self.assertRaises(ValueError):
            portal.send_email(
                recipient="bob@plone.org",
                sender="noreply@plone.org",
                subject="Trappist",
                body=u"One for you Bob!",
            )

    @mock.patch('plone.api.portal.parseaddr')
    def test_send_email_parseaddr(self, mock_parseaddr):
        """Simulate faulty parsing in parseaddr, from_address should be
        default email_from_address.
        """

        self.mailhost.reset()

        mock_parseaddr.return_value = ('Chuck Norris', 'chuck@norris.org')
        portal.send_email(
            recipient="bob@plone.org",
            subject="Trappist",
            body=u"One for you Bob!",
        )

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
            datetime=DateTime(1999, 12, 31, 23, 59),
            long_format=True,
        )
        self.assertEqual(result, 'Dec 31, 1999 11:59 PM')

        result = portal.get_localized_time(
            datetime=DateTime(1999, 12, 31, 23, 59),
            time_only=True,
        )
        self.assertEqual(result, '11:59 PM')

        result = portal.get_localized_time(
            datetime=DateTime(1999, 12, 31, 23, 59),
        )
        self.assertEqual(result, 'Dec 31, 1999')

    def test_get_localized_time_python_datetime(self):
        """Test getting the localized time using Python datetime.datetime."""

        # set the expected localized date format
        self._set_localization_date_format()

        # tests
        result = portal.get_localized_time(
            datetime=datetime(1999, 12, 31, 23, 59),
            long_format=True,
        )
        self.assertEqual(result, 'Dec 31, 1999 11:59 PM')

        result = portal.get_localized_time(
            datetime=datetime(1999, 12, 31, 23, 59),
            time_only=True,
        )
        self.assertEqual(result, '11:59 PM')

        result = portal.get_localized_time(
            datetime=datetime(1999, 12, 31, 23, 59),
        )
        self.assertEqual(result, 'Dec 31, 1999')

    def test_get_localized_time_python_date(self):
        """Test getting the localized time using Python datetime.date."""

        # set the expected localized date format
        self._set_localization_date_format()

        # tests
        result = portal.get_localized_time(
            datetime=date(1999, 12, 31),
            long_format=True,
        )
        self.assertEqual(result, 'Dec 31, 1999')

        result = portal.get_localized_time(
            datetime=date(1999, 12, 31),
            time_only=True,
        )
        self.assertEqual(result, '')

        result = portal.get_localized_time(
            datetime=date(1999, 12, 31),
        )
        self.assertEqual(result, 'Dec 31, 1999')

    def test_show_message_constraints(self):
        """Test the constraints for show_message."""
        from plone.api.exc import MissingParameterError

        # When no parameters are given an error is raised
        with self.assertRaises(MissingParameterError):
            portal.show_message()

        # message and request are required
        with self.assertRaises(MissingParameterError):
            portal.show_message(request=self.layer['request'])

        with self.assertRaises(MissingParameterError):
            portal.show_message(message='Beer is brewing.')

    def test_show_message(self):
        """Test to see if message appears."""

        from Products.statusmessages.interfaces import IStatusMessage
        request = self.layer['request']
        portal.show_message(message='Blueberries!', request=request)
        messages = IStatusMessage(request)
        show = messages.show()
        self.assertEqual(len(show), 1)
        self.assertIn('Blueberries!', show[0].message)
        portal.show_message(message='One', request=request)
        portal.show_message(message='Two', request=request)
        messages = IStatusMessage(request)
        show = messages.show()
        self.assertEqual(len(show), 2)
        self.assertEqual(show[0].message, 'One')
        self.assertEqual(show[1].message, 'Two')

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
        registry.records['plone.api.norris_power'] = Record(
            field.TextLine(title=u"Chuck Norris' Power"))
        registry.records['plone.api.unset'] = Record(
            field.TextLine(title=u"An unset field"))
        registry['plone.api.norris_power'] = u'infinite'

        self.assertEqual(
            portal.get_registry_record('plone.api.norris_power'),
            u'infinite',
        )

        self.assertEqual(
            portal.get_registry_record('plone.api.unset'),
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
            portal.get_registry_record(name=dict({'foo': 'bar'}))

    def test_get_invalid_registry_record_msg(self):
        """Test that the error message from trying to get a
        nonexistant registry record produces an error message which
        lists known registry records.
        """
        from plone.api.exc import InvalidParameterError
        with self.assertRaises(InvalidParameterError) as cm:
            portal.get_registry_record(name='nonexistent.sharepoint.power')

        self.assertTrue(
            str(cm.exception).startswith(
                "Cannot find a record with name "
                "'nonexistent.sharepoint.power'.\n"
            )
        )

        # A selection of records which should exist in all plone versions
        should_be_theres = (
            "plone.app.discussion.interfaces.IDiscussionSettings.captcha",
            "plone.app.querystring.field.Creator.title",
            "plone.app.querystring.operation.int.largerThan.description",
            "plone.app.querystring.operation.selection.is.widget",
        )

        for should_be_there in should_be_theres:
            self.assertIn((should_be_there + '\n'), str(cm.exception))

    def test_set_valid_registry_record(self):
        """Test that setting a valid registry record succeeds."""
        registry = getUtility(IRegistry)
        registry.records['plone.api.plone_power'] = Record(
            field.TextLine(title=u"Plone's Power"))
        portal.set_registry_record('plone.api.plone_power', u'awesome')
        self.assertEqual(registry['plone.api.plone_power'], u'awesome')

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
                name='nonexistent.sharepoint.power',
                value=u'Zero',
            )

    def test_set_no_value_param_for_existing_record(self):
        """Test that calling portal.set_registry_record with a name
        parameter for an existing record, but without a value, raises
        an Exception.
        """
        registry = getUtility(IRegistry)
        registry.records['plone.api.plone_power'] = Record(
            field.TextLine(title=u"Plone's Power"))

        from plone.api.exc import MissingParameterError
        with self.assertRaises(MissingParameterError):
            portal.set_registry_record(name='plone.api.plone_power')

    def test_set_invalid_key_type_record(self):
        """Test that trying to set the value of a record by passing a
        list for the record name instead of a string, raises an error.
        """
        from plone.api.exc import InvalidParameterError
        with self.assertRaises(InvalidParameterError):
            portal.set_registry_record(
                name=['foo', 'bar'],
                value=u"baz",
            )
