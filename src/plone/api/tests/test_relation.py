# -*- coding: utf-8 -*-
"""Tests for plone.api.content."""

from plone import api
from plone.api.tests.base import INTEGRATION_TESTING

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

    def test_create_relation(self):
        """Test creating a relation."""
        # Check that there are no relations at first for the two objects we will test.
        relations = api.relation.get(source=self.about, target=self.blog, relationship="link")
        self.assertEqual(len(relations), 0)
        api.relation.create(
            source=self.about,
            target=self.blog,
            relationship='link',
        )
        relations = api.relation.get(source=self.about, target=self.blog, relationship="link")
        self.assertEqual(len(relations), 1)
        relation = relations[0]
        self.assertEqual(relation.from_object, self.about)
        self.assertEqual(relation.to_object, self.blog)

    def test_delete_constraints(self):
        """Test the constraints when deleting relations."""
        from plone.api.exc import InvalidParameterError

        # If source is given, it must be dexterity.
        app = self.layer["app"]
        app.portal_type = "ZopeRoot"
        with self.assertRaises(InvalidParameterError):
            api.relation.delete(source=app)

        # If target is given, it must be dexterity.
        with self.assertRaises(InvalidParameterError):
            api.relation.delete(target=app)

        # If relationship is given, it must be a string.
        with self.assertRaises(InvalidParameterError):
            api.relation.delete(relationship=42)

    def test_delete_relation(self):
        """Test deleting a relation."""
        api.relation.create(
            source=self.about,
            target=self.blog,
            relationship='link',
        )
        api.relation.delete(
            source=self.about,
            target=self.blog,
            relationship='link',
        )
        relations = api.relation.get(source=self.about, target=self.blog, relationship="link")
        self.assertEqual(len(relations), 0)


    def test_get_constraints(self):
        """Test the constraints when getting relations."""
        from plone.api.exc import InvalidParameterError

        # If source is given, it must be dexterity.
        app = self.layer["app"]
        app.portal_type = "ZopeRoot"
        with self.assertRaises(InvalidParameterError):
            api.relation.get(source=app)

        # If target is given, it must be dexterity.
        with self.assertRaises(InvalidParameterError):
            api.relation.get(target=app)

        # If relationship is given, it must be a string.
        with self.assertRaises(InvalidParameterError):
            api.relation.get(relationship=42)

    def test_get_relation(self):
        """Test getting a relation."""
        api.relation.create(
            source=self.about,
            target=self.blog,
            relationship='link',
        )
        api.relation.create(
            source=self.events,
            target=self.blog,
            relationship='link',
        )
        api.relation.create(
            source=self.about.team,
            target=self.events,
            relationship='team',
        )
        api.relation.create(
            source=self.events,
            target=self.portal.image,
            relationship='link',
        )
        self.assertEqual(len(api.relation.get(source=self.about)), 1)
        self.assertEqual(len(api.relation.get(target=self.blog)), 2)
        self.assertEqual(len(api.relation.get(relationship="link")), 3)

        self.assertEqual(len(api.relation.get(source=self.events)), 2)
        self.assertEqual(len(api.relation.get(relationship="team")), 1)
