"""Tests for plone.api.content with Python 3.9+ features."""

from typing import Optional, List, Dict, Any, Union
from plone import api
from plone.api.tests.base import INTEGRATION_TESTING
from plone.app.testing import login, logout, setRoles
from z3c.relationfield import RelationValue
from zc.relation.interfaces import ICatalog
from zope.component import getUtility

import unittest
from contextlib import contextmanager


@contextmanager
def temporary_user(portal, username: str, roles: List[str]) -> None:
    """Context manager for temporary user creation and login/logout."""
    api.user.create(email=f"{username}@plone.org", username=username)
    setRoles(portal, username, roles)
    logout()
    login(portal, username)
    try:
        yield
    finally:
        logout()


class TestPloneApiRelation(unittest.TestCase):
    """Unit tests for relations using plone.api"""

    layer = INTEGRATION_TESTING

    def setUp(self) -> None:
        """Create a portal structure for testing.

        Structure:
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
        """
        self.portal = self.layer["portal"]

        # Create top-level content
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

        # Create nested content in about section
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

        # Create nested content in events section
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

    def test_create_constraints(self) -> None:
        """Test the constraints when creating relations."""
        from plone.api.exc import InvalidParameterError
        from plone.api.exc import MissingParameterError

        # Test missing parameters
        with self.assertRaises(MissingParameterError):
            api.relation.create()

        with self.assertRaises(MissingParameterError):
            api.relation.create(
                target=self.blog,
                relationship="link",
            )

        with self.assertRaises(MissingParameterError):
            api.relation.create(
                source=self.about,
                relationship="link",
            )

        with self.assertRaises(MissingParameterError):
            api.relation.create(
                source=self.about,
                target=self.blog,
            )

        # Test invalid parameters
        app = self.layer["app"]
        test_cases = [
            (
                InvalidParameterError,
                {"source": app, "target": self.blog, "relationship": "link"},
                "source without portal_type",
            ),
            (
                InvalidParameterError,
                {"source": self.about, "target": app, "relationship": "link"},
                "target without portal_type",
            ),
            (
                InvalidParameterError,
                {"source": self.about, "target": self.blog, "relationship": 42},
                "non-string relationship",
            ),
        ]

        for exception, kwargs, msg in test_cases:
            with self.subTest(msg=msg):
                with self.assertRaises(exception):
                    api.relation.create(**kwargs)

    def test_create_relation(self) -> None:
        """Test creating a relation."""
        # Verify initial state
        relations = api.relation.get(
            source=self.about,
            target=self.blog,
            relationship="link",
        )
        self.assertEqual(len(relations), 0)

        # Create and verify relation
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

        # Test relation field handling
        self.assertEqual(self.about.relatedItems, [])
        api.relation.create(
            source=self.about,
            target=self.blog,
            relationship="relatedItems",
        )
        self.assertEqual(len(self.about.relatedItems), 1)
        self.assertIsInstance(self.about.relatedItems[0], RelationValue)

        # Test non-relation field
        self.assertEqual(self.about.description, "")
        api.relation.create(
            source=self.about,
            target=self.blog,
            relationship="description",
        )
        self.assertEqual(self.about.description, "")
        self.assertEqual(len(api.relation.get(source=self.about, target=self.blog)), 3)

    def test_delete_constraints(self) -> None:
        """Test the constraints when deleting relations."""
        from plone.api.exc import InvalidParameterError

        app = self.layer["app"]
        test_cases = [
            ({"source": app}, "source without portal_type"),
            ({"target": app}, "target without portal_type"),
            ({"relationship": 42}, "non-string relationship"),
        ]

        for kwargs, msg in test_cases:
            with self.subTest(msg=msg):
                with self.assertRaises(InvalidParameterError):
                    api.relation.delete(**kwargs)

    def test_delete_relation(self) -> None:
        """Test deleting a relation."""
        # Create relation
        api.relation.create(
            source=self.about,
            target=self.blog,
            relationship="link",
        )

        # Delete and verify
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

    def test_get_relation(self) -> None:
        """Test getting relations with various filters."""
        # Setup test relations
        test_relations = [
            (self.about, self.blog, "link"),
            (self.events, self.blog, "link"),
            (self.about.team, self.events, "team"),
            (self.events, self.portal.image, "link"),
        ]

        for source, target, relationship in test_relations:
            api.relation.create(
                source=source,
                target=target,
                relationship=relationship,
            )

        # Test various queries
        test_cases = [
            ({"source": self.about}, 1),
            ({"target": self.blog}, 2),
            ({"relationship": "link"}, 3),
            ({"source": self.about, "relationship": "link"}, 1),
            ({"source": self.about, "target": self.events}, 0),
            ({"source": self.about, "target": self.blog}, 1),
            ({"source": self.events}, 2),
            ({"relationship": "team"}, 1),
        ]

        for query, expected_count in test_cases:
            with self.subTest(query=query):
                relations = api.relation.get(**query)
                self.assertEqual(len(relations), expected_count)
                if relations:
                    self.assertIsInstance(relations[0], RelationValue)

    def test_restricted_relation(self) -> None:
        """Test relation visibility with different user permissions."""
        # Setup test relations
        test_relations = [
            (self.about, self.blog, "link"),
            (self.events, self.blog, "link"),
            (self.about.team, self.events, "team"),
            (self.events, self.portal.image, "link"),
        ]

        for source, target, relationship in test_relations:
            api.relation.create(
                source=source,
                target=target,
                relationship=relationship,
            )

        # Publish some content
        api.content.transition(self.events, to_state="published")
        api.content.transition(self.blog, to_state="published")

        # Verify admin access
        self.assertEqual(len(api.relation.get(relationship="link")), 3)

        # Test restricted access
        with temporary_user(self.portal, "bob", ["Member"]):
            self.assertEqual(len(api.relation.get(relationship="link")), 2)
            self.assertEqual(
                len(api.relation.get(relationship="link", unrestricted=True)), 3
            )