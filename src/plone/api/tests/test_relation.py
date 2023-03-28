"""Tests for plone.api.content."""

from plone import api
from plone.api.tests.base import INTEGRATION_TESTING
from plone.app.testing import login
from plone.app.testing import logout
from plone.app.testing import setRoles
from z3c.relationfield import RelationValue
from zc.relation.interfaces import ICatalog
from zope.component import getUtility

import unittest


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
        self.portal = self.layer["portal"]

        self.blog = api.content.create(
            type="Link",
            id="blog",
            container=self.portal,
        )
        self.about = api.content.create(
            type="Folder",
            id="about",
            container=self.portal,
        )
        self.events = api.content.create(
            type="Folder",
            id="events",
            container=self.portal,
        )

        self.team = api.content.create(
            container=self.about,
            type="Document",
            id="team",
        )
        self.contact = api.content.create(
            container=self.about,
            type="Document",
            id="contact",
        )

        self.training = api.content.create(
            container=self.events,
            type="Event",
            id="training",
        )
        self.conference = api.content.create(
            container=self.events,
            type="Event",
            id="conference",
        )
        self.sprint = api.content.create(
            container=self.events,
            type="Event",
            id="sprint",
        )

        self.image = api.content.create(
            container=self.portal,
            type="Image",
            id="image",
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
                relationship="link",
            )

        # Check the constraints for the target parameter
        with self.assertRaises(MissingParameterError):
            api.relation.create(
                source=self.about,
                relationship="link",
            )

        # Check the constraints for the relationship parameter
        with self.assertRaises(MissingParameterError):
            api.relation.create(
                source=self.about,
                target=self.blog,
            )

        # We require a source with portal_type
        app = self.layer["app"]
        with self.assertRaises(InvalidParameterError):
            api.relation.create(
                source=app,
                target=self.blog,
                relationship="link",
            )

        # We require a target with portal_type
        with self.assertRaises(InvalidParameterError):
            api.relation.create(
                source=self.about,
                target=app,
                relationship="link",
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
        # Check that there are no relations at first
        # for the two objects we will test.
        relations = api.relation.get(
            source=self.about,
            target=self.blog,
            relationship="link",
        )
        self.assertEqual(len(relations), 0)
        api.relation.create(
            source=self.about,
            target=self.blog,
            relationship="link",
        )
        relations = api.relation.get(
            source=self.about,
            target=self.blog,
            relationship="link",
        )
        self.assertEqual(len(relations), 1)
        relation = relations[0]
        self.assertEqual(relation.from_object, self.about)
        self.assertEqual(relation.to_object, self.blog)

        # create relation that uses a field
        self.assertEqual(self.about.relatedItems, [])
        api.relation.create(
            source=self.about,
            target=self.blog,
            relationship="relatedItems",
        )
        self.assertEqual(len(self.about.relatedItems), 1)
        self.assertIsInstance(self.about.relatedItems[0], RelationValue)

        # create relation with a fieldname that is no relationfield
        self.assertEqual(self.about.description, "")
        api.relation.create(
            source=self.about,
            target=self.blog,
            relationship="description",
        )
        self.assertEqual(self.about.description, "")
        self.assertEqual(len(api.relation.get(source=self.about, target=self.blog)), 3)

    def test_delete_constraints(self):
        """Test the constraints when deleting relations."""
        from plone.api.exc import InvalidParameterError

        # If source is given, it must have a portal_type.
        app = self.layer["app"]
        with self.assertRaises(InvalidParameterError):
            api.relation.delete(source=app)

        # If target is given, it must have a portal_type.
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
            relationship="link",
        )
        api.relation.delete(
            source=self.about,
            target=self.blog,
            relationship="link",
        )
        relations = api.relation.get(
            source=self.about,
            target=self.blog,
            relationship="link",
        )
        self.assertEqual(len(relations), 0)

    def test_delete_fieldrelation(self):
        """Test deleting a relation that uses a relationlistfield."""
        api.relation.create(
            source=self.about,
            target=self.blog,
            relationship="link",
        )
        api.relation.create(
            source=self.about,
            target=self.blog,
            relationship="relatedItems",
        )
        self.assertEqual(len(api.relation.get(source=self.about)), 2)
        self.assertIsInstance(self.about.relatedItems[0], RelationValue)

        api.relation.delete(
            source=self.about,
            target=self.blog,
            relationship="relatedItems",
        )
        self.assertEqual(len(api.relation.get(source=self.about)), 1)
        self.assertEqual(len(self.about.relatedItems), 0)

    def test_delete_one_fieldrelation(self):
        """Test deleting a relation from a relationlistfield retains the others."""
        api.relation.create(
            source=self.about,
            target=self.blog,
            relationship="link",
        )
        api.relation.create(
            source=self.about,
            target=self.blog,
            relationship="relatedItems",
        )
        api.relation.create(
            source=self.about,
            target=self.events,
            relationship="relatedItems",
        )
        self.assertEqual(len(api.relation.get(source=self.about)), 3)
        self.assertIsInstance(self.about.relatedItems[0], RelationValue)

        api.relation.delete(
            source=self.about,
            target=self.blog,
            relationship="relatedItems",
        )
        self.assertEqual(len(api.relation.get(source=self.about)), 2)
        self.assertEqual(len(self.about.relatedItems), 1)

    def test_delete_by_relation(self):
        """Test deleting relations by relation name."""
        api.relation.create(
            source=self.about,
            target=self.blog,
            relationship="relatedItems",
        )
        api.relation.create(
            source=self.about,
            target=self.events,
            relationship="relatedItems",
        )
        self.assertEqual(len(api.relation.get(source=self.about)), 2)

        api.relation.delete(
            relationship="relatedItems",
        )
        self.assertEqual(len(api.relation.get(source=self.about)), 0)
        self.assertEqual(len(self.about.relatedItems), 0)

    def test_delete_by_source_and_relation(self):
        """Test deleting relations by source and relation name."""
        api.relation.create(
            source=self.about,
            target=self.blog,
            relationship="relatedItems",
        )
        api.relation.create(
            source=self.about,
            target=self.events,
            relationship="relatedItems",
        )
        api.relation.create(
            source=self.blog,
            target=self.events,
            relationship="relatedItems",
        )
        self.assertEqual(len(api.relation.get(relationship="relatedItems")), 3)

        api.relation.delete(
            source=self.about,
            relationship="relatedItems",
        )
        self.assertEqual(len(api.relation.get(relationship="relatedItems")), 1)

    def test_delete_by_target_and_relation(self):
        """Test deleting relations by target and relation name."""
        api.relation.create(
            source=self.about,
            target=self.blog,
            relationship="relatedItems",
        )
        api.relation.create(
            source=self.about,
            target=self.events,
            relationship="relatedItems",
        )
        api.relation.create(
            source=self.blog,
            target=self.events,
            relationship="relatedItems",
        )
        api.relation.create(
            source=self.blog,
            target=self.events,
            relationship="link",
        )
        self.assertEqual(len(api.relation.get(relationship="relatedItems")), 3)
        self.assertEqual(len(api.relation.get(relationship="link")), 1)

        api.relation.delete(
            target=self.events,
            relationship="relatedItems",
        )
        self.assertEqual(len(api.relation.get(relationship="relatedItems")), 1)
        self.assertEqual(len(api.relation.get(relationship="link")), 1)

    def test_delete_by_source(self):
        """Test deleting relations by source."""
        api.relation.create(
            source=self.about,
            target=self.blog,
            relationship="relatedItems",
        )
        api.relation.create(
            source=self.blog,
            target=self.events,
            relationship="relatedItems",
        )
        api.relation.create(
            source=self.about,
            target=self.blog,
            relationship="link",
        )
        api.relation.create(
            source=self.blog,
            target=self.events,
            relationship="link",
        )
        self.assertEqual(len(api.relation.get(relationship="relatedItems")), 2)
        self.assertEqual(len(api.relation.get(relationship="link")), 2)

        api.relation.delete(
            source=self.about,
        )
        self.assertEqual(len(api.relation.get(relationship="relatedItems")), 1)
        self.assertEqual(len(api.relation.get(relationship="link")), 1)

    def test_delete_by_target(self):
        """Test deleting relations by target."""
        api.relation.create(
            source=self.about,
            target=self.blog,
            relationship="relatedItems",
        )
        api.relation.create(
            source=self.blog,
            target=self.events,
            relationship="relatedItems",
        )
        api.relation.create(
            source=self.team,
            target=self.events,
            relationship="relatedItems",
        )
        api.relation.create(
            source=self.about,
            target=self.blog,
            relationship="link",
        )
        api.relation.create(
            source=self.blog,
            target=self.events,
            relationship="link",
        )
        self.assertEqual(len(api.relation.get(relationship="relatedItems")), 3)
        self.assertEqual(len(api.relation.get(relationship="link")), 2)

        api.relation.delete(
            target=self.events,
        )
        self.assertEqual(len(api.relation.get(relationship="relatedItems")), 1)
        self.assertEqual(len(api.relation.get(relationship="link")), 1)

    def test_deleted_relation_is_purged(self):
        """Test that relations that have the name of a non-relation-field are purged."""
        relation_catalog = getUtility(ICatalog)
        api.relation.create(
            source=self.about,
            target=self.blog,
            relationship="description",
        )
        self.assertEqual(self.about.description, "")
        self.assertEqual(len(api.relation.get(source=self.about)), 1)
        rels = relation_catalog.findRelations({"from_attribute": "description"})
        self.assertEqual(len([i for i in rels]), 1)

        api.relation.delete(
            source=self.about,
            target=self.blog,
            relationship="description",
        )
        self.assertEqual(len(api.relation.get(source=self.about)), 0)
        self.assertEqual(self.about.description, "")
        rels = relation_catalog.findRelations({"from_attribute": "description"})
        self.assertEqual(len([i for i in rels]), 0)

    def test_get_constraints(self):
        """Test the constraints when getting relations."""
        from plone.api.exc import InvalidParameterError

        # If source is given, it must have a portal_type.
        app = self.layer["app"]
        with self.assertRaises(InvalidParameterError):
            api.relation.get(source=app)

        # If target is given, it must have a portal_type.
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
            relationship="link",
        )
        api.relation.create(
            source=self.events,
            target=self.blog,
            relationship="link",
        )
        api.relation.create(
            source=self.about.team,
            target=self.events,
            relationship="team",
        )
        api.relation.create(
            source=self.events,
            target=self.portal.image,
            relationship="link",
        )
        self.assertEqual(len(api.relation.get(source=self.about)), 1)
        self.assertIsInstance(api.relation.get(source=self.about), list)
        self.assertIsInstance(api.relation.get(source=self.about)[0], RelationValue)

        self.assertEqual(len(api.relation.get(target=self.blog)), 2)
        self.assertEqual(len(api.relation.get(relationship="link")), 3)

        self.assertEqual(
            len(api.relation.get(source=self.about, relationship="link")), 1
        )
        self.assertEqual(
            len(api.relation.get(source=self.about, target=self.events)), 0
        )
        self.assertEqual(len(api.relation.get(source=self.about, target=self.blog)), 1)

        self.assertEqual(len(api.relation.get(source=self.events)), 2)
        self.assertEqual(len(api.relation.get(relationship="team")), 1)

    def test_get_relation_as_dict(self):
        """Test getting relations as dicts"""
        api.relation.create(
            source=self.about,
            target=self.blog,
            relationship="link",
        )
        api.relation.create(
            source=self.events,
            target=self.blog,
            relationship="bloglink",
        )
        self.assertEqual(
            len(api.relation.get(relationship="link", as_dict=True)["link"]), 1
        )
        rels = api.relation.get(target=self.blog, as_dict=True)
        self.assertEqual(len(rels["link"]), 1)
        self.assertEqual(len(rels["bloglink"]), 1)

    def test_get_broken_relation(self):
        """Test that broken relations are ignored."""
        api.relation.create(
            source=self.about,
            target=self.blog,
            relationship="link",
        )
        api.relation.create(
            source=self.events,
            target=self.portal.image,
            relationship="link",
        )
        self.assertEqual(len(api.relation.get(source=self.about)), 1)
        self.assertEqual(len(api.relation.get(relationship="link")), 2)

        # break a relation
        self.portal._delObject("blog")

        self.assertEqual(len(api.relation.get(source=self.about)), 0)
        self.assertEqual(len(api.relation.get(relationship="link")), 1)

    def test_restricted_relation(self):
        """Test that rels between inaccessible items are ignored."""
        api.relation.create(
            source=self.about,
            target=self.blog,
            relationship="link",
        )
        api.relation.create(
            source=self.events,
            target=self.blog,
            relationship="link",
        )
        api.relation.create(
            source=self.about.team,
            target=self.events,
            relationship="team",
        )
        api.relation.create(
            source=self.events,
            target=self.portal.image,
            relationship="link",
        )
        api.content.transition(self.events, to_state="published")
        api.content.transition(self.blog, to_state="published")
        self.assertEqual(len(api.relation.get(relationship="link")), 3)

        # Switch user
        api.user.create(email="bob@plone.org", username="bob")
        setRoles(self.portal, "bob", ["Member"])
        logout()
        login(self.portal, "bob")

        self.assertEqual(len(api.relation.get(relationship="link")), 2)
        self.assertEqual(
            len(api.relation.get(relationship="link", unrestricted=True)), 3
        )
