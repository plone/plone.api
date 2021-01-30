# -*- coding: utf-8 -*-
"""Tests for plone.api.content."""

from Acquisition import aq_base
from OFS.CopySupport import CopyError
from OFS.event import ObjectWillBeMovedEvent
from OFS.interfaces import IObjectWillBeMovedEvent
from plone import api
from plone.api.content import NEW_LINKINTEGRITY
from plone.api.tests.base import INTEGRATION_TESTING
from plone.app.layout.navigation.interfaces import INavigationRoot
from plone.app.linkintegrity.exceptions import LinkIntegrityNotificationException  # NOQA: E501
from plone.app.textfield import RichTextValue
from plone.dexterity.interfaces import IDexterityContent
from plone.indexer import indexer
from plone.uuid.interfaces import IMutableUUID
from plone.uuid.interfaces import IUUIDGenerator
from Products.CMFCore.interfaces import IContentish
from Products.CMFCore.WorkflowCore import WorkflowException
from Products.ZCatalog.interfaces import IZCatalog
from zExceptions import BadRequest
from zope.component import getGlobalSiteManager
from zope.component import getUtility
from zope.container.contained import ContainerModifiedEvent
from zope.interface import alsoProvides
from zope.lifecycleevent import IObjectModifiedEvent
from zope.lifecycleevent import IObjectMovedEvent
from zope.lifecycleevent import modified
from zope.lifecycleevent import ObjectMovedEvent

import mock
import pkg_resources
import six
import unittest


try:
    pkg_resources.get_distribution('plone.app.contenttypes')
except pkg_resources.DistributionNotFound:
    HAS_PACONTENTYPES = False
else:
    HAS_PACONTENTYPES = True


class TestPloneApiRelation(unittest.TestCase):
    """Unit tests for relations using plone.api"""

    layer = INTEGRATION_TESTING

    def setUp(self):
        """Create a portal structure which we can test against.

        Plone (portal root)
        |-- image
        |-- blog
        |-- about
        |   |-- team
        |   `-- contact
        `-- events
            |-- training
            |-- conference
            `-- sprint

        This is copied from test_content.py.
        We may want to simplify.  But could be okay.
        """
        self.portal = self.layer['portal']

        self.blog = api.content.create(
            type='Link',
            id='blog',
            container=self.portal,
        )
        self.about = api.content.create(
            type='Folder',
            id='about',
            container=self.portal,
        )
        self.events = api.content.create(
            type='Folder',
            id='events',
            container=self.portal,
        )

        self.team = api.content.create(
            container=self.about,
            type='Document',
            id='team',
        )
        self.contact = api.content.create(
            container=self.about,
            type='Document',
            id='contact',
        )

        self.training = api.content.create(
            container=self.events,
            type='Event',
            id='training',
        )
        self.conference = api.content.create(
            container=self.events,
            type='Event',
            id='conference',
        )
        self.sprint = api.content.create(
            container=self.events,
            type='Event',
            id='sprint',
        )

        self.image = api.content.create(
            container=self.portal,
            type='Image',
            id='image',
        )

    def test_create_constraints(self):
        """Test the constraints when creating relations."""
        from plone.api.exc import InvalidParameterError
        from plone.api.exc import MissingParameterError

        # This will definitely fail
        with self.assertRaises(MissingParameterError):
            api.relation.create()

        # Check the constraints for the source parameter
        with self.assertRaises(MissingParameterError):
            api.relation.create(
                target=self.blog,
                relationship='link',
            )

        # Check the constraints for the target parameter
        with self.assertRaises(MissingParameterError):
            api.relation.create(
                source=self.about,
                relationship='link',
            )

        # Check the constraints for the relationship parameter
        with self.assertRaises(MissingParameterError):
            api.relation.create(
                source=self.about,
                target=self.blog,
            )

        # We require a dexterity source
        app = self.layer["app"]
        app.portal_type = "ZopeRoot"
        with self.assertRaises(InvalidParameterError):
            api.relation.create(
                source=app,
                target=self.blog,
                relationship='link',
            )

        # We require a dexterity target
        with self.assertRaises(InvalidParameterError):
            api.relation.create(
                source=self.about,
                target=app,
                relationship='link',
            )

        # We require a string relationship
        with self.assertRaises(InvalidParameterError):
            api.relation.create(
                source=self.about,
                target=self.blog,
                relationship=42,
            )
