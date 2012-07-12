# -*- coding: utf-8 -*-
"""Tests for plone.api.portal."""

from email import message_from_string
import mock
import unittest

from DateTime import DateTime
from Products.CMFCore.utils import getToolByName
from Products.CMFPlone.tests.utils import MockMailHost
from Products.MailHost.interfaces import IMailHost

from plone.api import portal
from plone.api.tests.base import INTEGRATION_TESTING


class TestPloneApiPortal(unittest.TestCase):
    """Unit tests for getting portal info using plone.api"""

    layer = INTEGRATION_TESTING

    def setUp(self):
        """  """
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
        self.assertEqual(portal.get(), self.portal)

    def test_url(self):
        self.assertEqual(portal.url(), 'http://nohost/plone')

    def test_get_tool_constraints(self):
        """ Test the constraints for getting a tool. """

        # When no parameters are given an error is raised
        self.assertRaises(ValueError, portal.get_tool)

    def test_get_tool(self):
        self.assertEqual(portal.get_tool(name='portal_catalog'),
            getToolByName(self.portal, 'portal_catalog'))
        self.assertEqual(portal.get_tool(name='portal_membership'),
            getToolByName(self.portal, 'portal_membership'))
        self.assertRaises(AttributeError, portal.get_tool, name='non_existing')

    def test_send_email_constraints(self):
        """ Test the constraints for sending an email. """

        # When no parameters are given an error is raised
        self.assertRaises(ValueError, portal.send_email)

        # recipient, subject and body are required
        self.assertRaises(ValueError, portal.send_email, subject='Beer',
            body="To beer or not to beer, that is the question")
        self.assertRaises(ValueError, portal.send_email,
            recipient='joe@example.org', subject='Beer')
        self.assertRaises(ValueError, portal.send_email,
            recipient='joe@example.org',
            body="To beer or not to beer, that is the question")

    def test_send_email(self):
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
        """ By default, the MailHost is not configured yet, so we cannot
        send email.
        """
        self.portal._updateProperty('email_from_address', None)
        self.assertRaises(ValueError, portal.send_email,
            recipient="bob@plone.org",
            sender="noreply@plone.org",
            subject="Trappist",
            body=u"One for you Bob!")

    @mock.patch('plone.api.portal.parseaddr')
    def test_send_email_parseaddr(self, mock_parseaddr):
        """ Simulate faulty parsing in parseaddr, from_address should be
        default email_from_address.
        """

        self.mailhost.reset()

        mock_parseaddr.return_value = ('Chuck Norris', 'chuck@norris.org')
        portal.send_email(
            recipient="bob@plone.org",
            subject="Trappist",
            body=u"One for you Bob!",
        )

    def test_localized_time_constraints(self):
        """ Test the constraints for localized_time. """

        # When no parameters are given an error is raised
        self.assertRaises(ValueError, portal.localized_time)

        # datetime and request are required
        self.assertRaises(ValueError, portal.localized_time,
                          datetime=DateTime())
        self.assertRaises(ValueError, portal.localized_time,
                          request=self.layer['request'])

    def test_localized_time(self):
        request = self.layer['request']
        result = portal.localized_time(datetime=DateTime(1999, 12, 31, 23, 59),
            request=request, long_format=True, time_only=False)
        self.assertEqual(result, 'Dec 31, 1999 11:59 PM')
        result = portal.localized_time(datetime=DateTime(1999, 12, 31, 23, 59),
            request=request, time_only=True)
        self.assertEqual(result, '11:59 PM')
        result = portal.localized_time(datetime=DateTime(1999, 12, 31, 23, 59),
            request=request)
        self.assertEqual(result, 'Dec 31, 1999')

    def test_show_message_constraints(self):
        """ Test the constraints for show_message. """

        # When no parameters are given an error is raised
        self.assertRaises(ValueError, portal.show_message)

        # message and request are required
        self.assertRaises(ValueError, portal.show_message,
                          request=self.layer['request'])
        self.assertRaises(ValueError, portal.show_message,
                          message='Beer is brewing.')

    def test_show_message(self):
        from Products.statusmessages.interfaces import IStatusMessage
        request = self.layer['request']
        portal.show_message(message='Blueberries!', request=request)
        messages = IStatusMessage(request)
        show = messages.show()
        self.assertEquals(len(show), 1)
        self.assertTrue('Blueberries!' in show[0].message)
        portal.show_message(message='One', request=request)
        portal.show_message(message='Two', request=request)
        messages = IStatusMessage(request)
        show = messages.show()
        self.assertEqual(len(show), 2)
        self.assertEqual(show[0].message, 'One')
        self.assertEqual(show[1].message, 'Two')
