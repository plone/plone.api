# -*- coding: utf-8 -*-
"""Tests for plone.api.portal."""

from DateTime import DateTime
from email import message_from_string
from plone.api import portal
from plone.api.exc import InvalidParameterError
from plone.api.exc import MissingParameterError
from plone.api.tests.base import INTEGRATION_TESTING
from plone.app.layout.navigation.interfaces import INavigationRoot
from plone.registry import field
from plone.registry.interfaces import IRegistry
from plone.registry.record import Record
from Products.CMFCore.utils import getToolByName
from Products.CMFPlone.tests.utils import MockMailHost
from Products.MailHost.interfaces import IMailHost
from zope.component import getUtility

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

        self.mailhost = getToolByName(self.portal, 'MailHost')

        self.portal._updateProperty('email_from_name', 'Portal Owner')
        self.portal._updateProperty('email_from_address', 'sender@example.org')

    def test_get(self):
        """Test getting the portal object."""
        self.assertEqual(portal.get(), self.portal)

    @mock.patch('plone.api.portal.getSite')
    def test_get_no_site(self, getSite):
        """Test error msg when getSite() returns None."""
        getSite.return_value = None
        from plone.api.exc import CannotGetPortalError
        self.assertRaises(CannotGetPortalError, portal.get)

    def test_get_tool_constraints(self):
        """Test the constraints for getting a tool."""

        # When no parameters are given an error is raised
        self.assertRaises(MissingParameterError, portal.get_tool)

    def test_get_tool_tool_not_found(self):
        """Test that error msg lists available tools if a tool is not found."""

        with self.assertRaises(InvalidParameterError) as cm:
            portal.get_tool('portal_foo')

        self.maxDiff = None  # to see assert diff
        self.assertMultiLineEqual(
            cm.exception.message,
            "Cannot find a tool with name 'portal_foo'. \n"
            "Available tools are:\n"
            "portal_setup\n"
            "portal_actionicons\n"
            "portal_actions\n"
            "portal_atct\n"
            "portal_calendar\n"
            "portal_catalog\n"
            "portal_controlpanel\n"
            "portal_css\n"
            "portal_diff\n"
            "portal_factory\n"
            "portal_groupdata\n"
            "portal_groups\n"
            "portal_interface\n"
            "portal_javascripts\n"
            "portal_kss\n"
            "portal_memberdata\n"
            "portal_membership\n"
            "portal_metadata\n"
            "portal_migration\n"
            "portal_password_reset\n"
            "portal_properties\n"
            "portal_quickinstaller\n"
            "portal_registration\n"
            "portal_skins\n"
            "portal_syndication\n"
            "portal_types\n"
            "portal_uidannotation\n"
            "portal_uidgenerator\n"
            "portal_uidhandler\n"
            "portal_undo\n"
            "portal_url\n"
            "portal_view_customizations\n"
            "portal_workflow\n"
            "portal_form_controller\n"
            "portal_transforms\n"
            "portal_archivist\n"
            "portal_historiesstorage\n"
            "portal_historyidhandler\n"
            "portal_modifier\n"
            "portal_purgepolicy\n"
            "portal_referencefactories\n"
            "portal_repository\n"
            "portal_languages\n"
            "portal_tinymce\n"
            "portal_registry\n"
            "portal_discussion"
        )

    def test_get_tool(self):
        """Test to validate the tool name."""

        self.assertEqual(
            portal.get_tool(name='portal_catalog'),
            getToolByName(self.portal, 'portal_catalog')
        )
        self.assertEqual(
            portal.get_tool(name='portal_membership'),
            getToolByName(self.portal, 'portal_membership')
        )

    def test_send_email_constraints(self):
        """Test the constraints for sending an email."""

        # When no parameters are given an error is raised
        self.assertRaises(ValueError, portal.send_email)

        # recipient, subject and body are required
        self.assertRaises(
            ValueError,
            portal.send_email,
            subject='Beer',
            body="To beer or not to beer, that is the question"
        )
        self.assertRaises(
            ValueError,
            portal.send_email,
            recipient='joe@example.org',
            subject='Beer'
        )
        self.assertRaises(
            ValueError,
            portal.send_email,
            recipient='joe@example.org',
            body="To beer or not to beer, that is the question"
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
        self.assertRaises(
            ValueError,
            portal.send_email,
            recipient="bob@plone.org",
            sender="noreply@plone.org",
            subject="Trappist",
            body=u"One for you Bob!"
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
        self.assertRaises(ValueError, portal.get_localized_time)

    def test_get_localized_time(self):
        """Test getting the localized time."""
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

    def test_show_message_constraints(self):
        """Test the constraints for show_message."""

        # When no parameters are given an error is raised
        self.assertRaises(ValueError, portal.show_message)

        # message and request are required
        self.assertRaises(ValueError, portal.show_message,
                          request=self.layer['request'])
        self.assertRaises(ValueError, portal.show_message,
                          message='Beer is brewing.')

    def test_show_message(self):
        """Test to see if message appears."""

        from Products.statusmessages.interfaces import IStatusMessage
        request = self.layer['request']
        portal.show_message(message='Blueberries!', request=request)
        messages = IStatusMessage(request)
        show = messages.show()
        self.assertEqual(len(show), 1)
        self.assertTrue('Blueberries!' in show[0].message)
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
        self.assertRaises(ValueError, portal.get_navigation_root)

    def test_get_registry_record(self):
        registry = getUtility(IRegistry)
        registry.records['plone.api.norris_power'] = Record(
            field.TextLine(title=u"Chuck Norris' Power"))
        registry['plone.api.norris_power'] = u'infinite'

        self.assertRaises(KeyError, portal.get_registry_record,
                          name='nonexistent.sharepoint.power')
        self.assertRaises(MissingParameterError, portal.get_registry_record)
        self.assertRaises(InvalidParameterError, portal.get_registry_record,
                          name=dict({'foo': 'bar'}))
        self.assertEqual(portal.get_registry_record('plone.api.norris_power'),
                         u'infinite')

    def test_set_registry_record(self):
        registry = getUtility(IRegistry)
        registry.records['plone.api.plone_power'] = Record(
            field.TextLine(title=u"Plone's Power"))
        portal.set_registry_record('plone.api.plone_power', u'awesome')
        self.assertEqual(registry['plone.api.plone_power'], u'awesome')
        self.assertRaises(KeyError, portal.set_registry_record,
                          name='nonexistent.sharepoint.power',
                          value=u'Zero')
        self.assertRaises(MissingParameterError, portal.set_registry_record)
        self.assertRaises(MissingParameterError, portal.set_registry_record,
                          name='plone.api.plone_power')
        self.assertRaises(InvalidParameterError, portal.set_registry_record,
                          name=['foo', 'bar'],
                          value=u"baz")
