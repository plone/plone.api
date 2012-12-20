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
            "Cannot find a tool with name 'portal_foo'.\n"
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

        with self.assertRaises(MissingParameterError):
            portal.get_registry_record()

        with self.assertRaises(InvalidParameterError):
            portal.get_registry_record(name=dict({'foo': 'bar'}))

        with self.assertRaises(InvalidParameterError) as cm:
            portal.get_registry_record(name='nonexistent.sharepoint.power')

        self.maxDiff = None  # to see assert diff
        self.assertMultiLineEqual(
            cm.exception.message,
            "Cannot find a record with name 'nonexistent.sharepoint.power'.\n"
            "Available records are:\n"
            "Products.ResourceRegistries.interfaces.settings.IResourceRegistriesSettings.resourceBundlesForThemes\n"
            "plone.api.norris_power\n"
            "plone.api.unset\n"
            "plone.app.discussion.interfaces.IDiscussionSettings.anonymous_comments\n"
            "plone.app.discussion.interfaces.IDiscussionSettings.captcha\n"
            "plone.app.discussion.interfaces.IDiscussionSettings.globally_enabled\n"
            "plone.app.discussion.interfaces.IDiscussionSettings.moderation_enabled\n"
            "plone.app.discussion.interfaces.IDiscussionSettings.moderator_email\n"
            "plone.app.discussion.interfaces.IDiscussionSettings.moderator_notification_enabled\n"
            "plone.app.discussion.interfaces.IDiscussionSettings.show_commenter_image\n"
            "plone.app.discussion.interfaces.IDiscussionSettings.text_transform\n"
            "plone.app.discussion.interfaces.IDiscussionSettings.user_notification_enabled\n"
            "plone.app.querystring.field.Creator.description\n"
            "plone.app.querystring.field.Creator.enabled\n"
            "plone.app.querystring.field.Creator.group\n"
            "plone.app.querystring.field.Creator.operations\n"
            "plone.app.querystring.field.Creator.sortable\n"
            "plone.app.querystring.field.Creator.title\n"
            "plone.app.querystring.field.Creator.vocabulary\n"
            "plone.app.querystring.field.Description.description\n"
            "plone.app.querystring.field.Description.enabled\n"
            "plone.app.querystring.field.Description.group\n"
            "plone.app.querystring.field.Description.operations\n"
            "plone.app.querystring.field.Description.sortable\n"
            "plone.app.querystring.field.Description.title\n"
            "plone.app.querystring.field.Description.vocabulary\n"
            "plone.app.querystring.field.SearchableText.description\n"
            "plone.app.querystring.field.SearchableText.enabled\n"
            "plone.app.querystring.field.SearchableText.group\n"
            "plone.app.querystring.field.SearchableText.operations\n"
            "plone.app.querystring.field.SearchableText.sortable\n"
            "plone.app.querystring.field.SearchableText.title\n"
            "plone.app.querystring.field.SearchableText.vocabulary\n"
            "plone.app.querystring.field.Subject.description\n"
            "plone.app.querystring.field.Subject.enabled\n"
            "plone.app.querystring.field.Subject.group\n"
            "plone.app.querystring.field.Subject.operations\n"
            "plone.app.querystring.field.Subject.sortable\n"
            "plone.app.querystring.field.Subject.title\n"
            "plone.app.querystring.field.Subject.vocabulary\n"
            "plone.app.querystring.field.Title.description\n"
            "plone.app.querystring.field.Title.enabled\n"
            "plone.app.querystring.field.Title.group\n"
            "plone.app.querystring.field.Title.operations\n"
            "plone.app.querystring.field.Title.sortable\n"
            "plone.app.querystring.field.Title.title\n"
            "plone.app.querystring.field.Title.vocabulary\n"
            "plone.app.querystring.field.created.description\n"
            "plone.app.querystring.field.created.enabled\n"
            "plone.app.querystring.field.created.group\n"
            "plone.app.querystring.field.created.operations\n"
            "plone.app.querystring.field.created.sortable\n"
            "plone.app.querystring.field.created.title\n"
            "plone.app.querystring.field.created.vocabulary\n"
            "plone.app.querystring.field.effective.description\n"
            "plone.app.querystring.field.effective.enabled\n"
            "plone.app.querystring.field.effective.group\n"
            "plone.app.querystring.field.effective.operations\n"
            "plone.app.querystring.field.effective.sortable\n"
            "plone.app.querystring.field.effective.title\n"
            "plone.app.querystring.field.effective.vocabulary\n"
            "plone.app.querystring.field.effectiveRange.description\n"
            "plone.app.querystring.field.effectiveRange.enabled\n"
            "plone.app.querystring.field.effectiveRange.group\n"
            "plone.app.querystring.field.effectiveRange.operations\n"
            "plone.app.querystring.field.effectiveRange.sortable\n"
            "plone.app.querystring.field.effectiveRange.title\n"
            "plone.app.querystring.field.effectiveRange.vocabulary\n"
            "plone.app.querystring.field.end.description\n"
            "plone.app.querystring.field.end.enabled\n"
            "plone.app.querystring.field.end.group\n"
            "plone.app.querystring.field.end.operations\n"
            "plone.app.querystring.field.end.sortable\n"
            "plone.app.querystring.field.end.title\n"
            "plone.app.querystring.field.end.vocabulary\n"
            "plone.app.querystring.field.expires.description\n"
            "plone.app.querystring.field.expires.enabled\n"
            "plone.app.querystring.field.expires.group\n"
            "plone.app.querystring.field.expires.operations\n"
            "plone.app.querystring.field.expires.sortable\n"
            "plone.app.querystring.field.expires.title\n"
            "plone.app.querystring.field.expires.vocabulary\n"
            "plone.app.querystring.field.getId.description\n"
            "plone.app.querystring.field.getId.enabled\n"
            "plone.app.querystring.field.getId.group\n"
            "plone.app.querystring.field.getId.operations\n"
            "plone.app.querystring.field.getId.sortable\n"
            "plone.app.querystring.field.getId.title\n"
            "plone.app.querystring.field.getId.vocabulary\n"
            "plone.app.querystring.field.getObjPositionInParent.description\n"
            "plone.app.querystring.field.getObjPositionInParent.enabled\n"
            "plone.app.querystring.field.getObjPositionInParent.group\n"
            "plone.app.querystring.field.getObjPositionInParent.operations\n"
            "plone.app.querystring.field.getObjPositionInParent.sortable\n"
            "plone.app.querystring.field.getObjPositionInParent.title\n"
            "plone.app.querystring.field.getObjPositionInParent.vocabulary\n"
            "plone.app.querystring.field.getRawRelatedItems.description\n"
            "plone.app.querystring.field.getRawRelatedItems.enabled\n"
            "plone.app.querystring.field.getRawRelatedItems.group\n"
            "plone.app.querystring.field.getRawRelatedItems.operations\n"
            "plone.app.querystring.field.getRawRelatedItems.sortable\n"
            "plone.app.querystring.field.getRawRelatedItems.title\n"
            "plone.app.querystring.field.getRawRelatedItems.vocabulary\n"
            "plone.app.querystring.field.isDefaultPage.description\n"
            "plone.app.querystring.field.isDefaultPage.enabled\n"
            "plone.app.querystring.field.isDefaultPage.group\n"
            "plone.app.querystring.field.isDefaultPage.operations\n"
            "plone.app.querystring.field.isDefaultPage.sortable\n"
            "plone.app.querystring.field.isDefaultPage.title\n"
            "plone.app.querystring.field.isDefaultPage.vocabulary\n"
            "plone.app.querystring.field.isFolderish.description\n"
            "plone.app.querystring.field.isFolderish.enabled\n"
            "plone.app.querystring.field.isFolderish.group\n"
            "plone.app.querystring.field.isFolderish.operations\n"
            "plone.app.querystring.field.isFolderish.sortable\n"
            "plone.app.querystring.field.isFolderish.title\n"
            "plone.app.querystring.field.isFolderish.vocabulary\n"
            "plone.app.querystring.field.modified.description\n"
            "plone.app.querystring.field.modified.enabled\n"
            "plone.app.querystring.field.modified.group\n"
            "plone.app.querystring.field.modified.operations\n"
            "plone.app.querystring.field.modified.sortable\n"
            "plone.app.querystring.field.modified.title\n"
            "plone.app.querystring.field.modified.vocabulary\n"
            "plone.app.querystring.field.path.description\n"
            "plone.app.querystring.field.path.enabled\n"
            "plone.app.querystring.field.path.group\n"
            "plone.app.querystring.field.path.operations\n"
            "plone.app.querystring.field.path.sortable\n"
            "plone.app.querystring.field.path.title\n"
            "plone.app.querystring.field.path.vocabulary\n"
            "plone.app.querystring.field.portal_type.description\n"
            "plone.app.querystring.field.portal_type.enabled\n"
            "plone.app.querystring.field.portal_type.group\n"
            "plone.app.querystring.field.portal_type.operations\n"
            "plone.app.querystring.field.portal_type.sortable\n"
            "plone.app.querystring.field.portal_type.title\n"
            "plone.app.querystring.field.portal_type.vocabulary\n"
            "plone.app.querystring.field.review_state.description\n"
            "plone.app.querystring.field.review_state.enabled\n"
            "plone.app.querystring.field.review_state.group\n"
            "plone.app.querystring.field.review_state.operations\n"
            "plone.app.querystring.field.review_state.sortable\n"
            "plone.app.querystring.field.review_state.title\n"
            "plone.app.querystring.field.review_state.vocabulary\n"
            "plone.app.querystring.field.sortable_title.description\n"
            "plone.app.querystring.field.sortable_title.enabled\n"
            "plone.app.querystring.field.sortable_title.group\n"
            "plone.app.querystring.field.sortable_title.operations\n"
            "plone.app.querystring.field.sortable_title.sortable\n"
            "plone.app.querystring.field.sortable_title.title\n"
            "plone.app.querystring.field.sortable_title.vocabulary\n"
            "plone.app.querystring.field.start.description\n"
            "plone.app.querystring.field.start.enabled\n"
            "plone.app.querystring.field.start.group\n"
            "plone.app.querystring.field.start.operations\n"
            "plone.app.querystring.field.start.sortable\n"
            "plone.app.querystring.field.start.title\n"
            "plone.app.querystring.field.start.vocabulary\n"
            "plone.app.querystring.operation.boolean.isFalse.description\n"
            "plone.app.querystring.operation.boolean.isFalse.operation\n"
            "plone.app.querystring.operation.boolean.isFalse.title\n"
            "plone.app.querystring.operation.boolean.isFalse.widget\n"
            "plone.app.querystring.operation.boolean.isTrue.description\n"
            "plone.app.querystring.operation.boolean.isTrue.operation\n"
            "plone.app.querystring.operation.boolean.isTrue.title\n"
            "plone.app.querystring.operation.boolean.isTrue.widget\n"
            "plone.app.querystring.operation.date.afterToday.description\n"
            "plone.app.querystring.operation.date.afterToday.operation\n"
            "plone.app.querystring.operation.date.afterToday.title\n"
            "plone.app.querystring.operation.date.afterToday.widget\n"
            "plone.app.querystring.operation.date.beforeToday.description\n"
            "plone.app.querystring.operation.date.beforeToday.operation\n"
            "plone.app.querystring.operation.date.beforeToday.title\n"
            "plone.app.querystring.operation.date.beforeToday.widget\n"
            "plone.app.querystring.operation.date.between.description\n"
            "plone.app.querystring.operation.date.between.operation\n"
            "plone.app.querystring.operation.date.between.title\n"
            "plone.app.querystring.operation.date.between.widget\n"
            "plone.app.querystring.operation.date.largerThan.description\n"
            "plone.app.querystring.operation.date.largerThan.operation\n"
            "plone.app.querystring.operation.date.largerThan.title\n"
            "plone.app.querystring.operation.date.largerThan.widget\n"
            "plone.app.querystring.operation.date.largerThanRelativeDate.description\n"
            "plone.app.querystring.operation.date.largerThanRelativeDate.operation\n"
            "plone.app.querystring.operation.date.largerThanRelativeDate.title\n"
            "plone.app.querystring.operation.date.largerThanRelativeDate.widget\n"
            "plone.app.querystring.operation.date.lessThan.description\n"
            "plone.app.querystring.operation.date.lessThan.operation\n"
            "plone.app.querystring.operation.date.lessThan.title\n"
            "plone.app.querystring.operation.date.lessThan.widget\n"
            "plone.app.querystring.operation.date.lessThanRelativeDate.description\n"
            "plone.app.querystring.operation.date.lessThanRelativeDate.operation\n"
            "plone.app.querystring.operation.date.lessThanRelativeDate.title\n"
            "plone.app.querystring.operation.date.lessThanRelativeDate.widget\n"
            "plone.app.querystring.operation.date.today.description\n"
            "plone.app.querystring.operation.date.today.operation\n"
            "plone.app.querystring.operation.date.today.title\n"
            "plone.app.querystring.operation.date.today.widget\n"
            "plone.app.querystring.operation.int.is.description\n"
            "plone.app.querystring.operation.int.is.operation\n"
            "plone.app.querystring.operation.int.is.title\n"
            "plone.app.querystring.operation.int.is.widget\n"
            "plone.app.querystring.operation.int.largerThan.description\n"
            "plone.app.querystring.operation.int.largerThan.operation\n"
            "plone.app.querystring.operation.int.largerThan.title\n"
            "plone.app.querystring.operation.int.largerThan.widget\n"
            "plone.app.querystring.operation.int.lessThan.description\n"
            "plone.app.querystring.operation.int.lessThan.operation\n"
            "plone.app.querystring.operation.int.lessThan.title\n"
            "plone.app.querystring.operation.int.lessThan.widget\n"
            "plone.app.querystring.operation.list.contains.description\n"
            "plone.app.querystring.operation.list.contains.operation\n"
            "plone.app.querystring.operation.list.contains.title\n"
            "plone.app.querystring.operation.list.contains.widget\n"
            "plone.app.querystring.operation.path.isWithin.description\n"
            "plone.app.querystring.operation.path.isWithin.operation\n"
            "plone.app.querystring.operation.path.isWithin.title\n"
            "plone.app.querystring.operation.path.isWithin.widget\n"
            "plone.app.querystring.operation.path.isWithinRelative.description\n"
            "plone.app.querystring.operation.path.isWithinRelative.operation\n"
            "plone.app.querystring.operation.path.isWithinRelative.title\n"
            "plone.app.querystring.operation.path.isWithinRelative.widget\n"
            "plone.app.querystring.operation.reference.is.description\n"
            "plone.app.querystring.operation.reference.is.operation\n"
            "plone.app.querystring.operation.reference.is.title\n"
            "plone.app.querystring.operation.reference.is.widget\n"
            "plone.app.querystring.operation.selection.is.description\n"
            "plone.app.querystring.operation.selection.is.operation\n"
            "plone.app.querystring.operation.selection.is.title\n"
            "plone.app.querystring.operation.selection.is.widget\n"
            "plone.app.querystring.operation.string.contains.description\n"
            "plone.app.querystring.operation.string.contains.operation\n"
            "plone.app.querystring.operation.string.contains.title\n"
            "plone.app.querystring.operation.string.contains.widget\n"
            "plone.app.querystring.operation.string.currentUser.description\n"
            "plone.app.querystring.operation.string.currentUser.operation\n"
            "plone.app.querystring.operation.string.currentUser.title\n"
            "plone.app.querystring.operation.string.currentUser.widget\n"
            "plone.app.querystring.operation.string.is.description\n"
            "plone.app.querystring.operation.string.is.operation\n"
            "plone.app.querystring.operation.string.is.title\n"
            "plone.app.querystring.operation.string.is.widget\n"
            "plone.app.querystring.operation.string.path.description\n"
            "plone.app.querystring.operation.string.path.operation\n"
            "plone.app.querystring.operation.string.path.title\n"
            "plone.app.querystring.operation.string.path.widget\n"
            "plone.app.querystring.operation.string.relativePath.description\n"
            "plone.app.querystring.operation.string.relativePath.operation\n"
            "plone.app.querystring.operation.string.relativePath.title\n"
            "plone.app.querystring.operation.string.relativePath.widget"
        )

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
