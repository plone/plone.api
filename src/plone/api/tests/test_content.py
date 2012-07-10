# -*- coding: utf-8 -*-
"""Tests for plone.api content."""
import mock
import unittest
from zExceptions import BadRequest

from plone.api import content
from plone.api.tests.base import INTEGRATION_TESTING


class TestPloneApiContent(unittest.TestCase):
    """Unit test on IWWBSearcher using mocked service results."""

    layer = INTEGRATION_TESTING

    def setUp(self):
        """  Create a site structure which we can test against:
        Plone (site root)
        |-- welcome
        |-- about
        |   |-- team
        |   `-- contact
        `-- events
            |-- training
            |-- conference
            `-- sprint

        """
        self.portal = self.layer['portal']
        self.portal.manage_delObjects([x.id for x in self.portal.getFolderContents()])  # Clean up

        self.welcome = content.create(type='Document', id='welcome', container=self.portal, strict=True)
        self.about = content.create(type='Folder', id='about', container=self.portal, strict=True)
        self.events = content.create(type='Folder', id='events', container=self.portal, strict=True)

        self.team = content.create(container=self.about, type='Document', id='team', strict=True)
        content.create(container=self.about, type='Document', id='contact', strict=True)

        content.create(container=self.events, type='Event', id='training', strict=True)
        content.create(container=self.events, type='Event', id='conference', strict=True)
        content.create(container=self.events, type='Event', id='sprint', strict=True)

    def test_create_constraints(self):
        """ Test the constraints when creating content """

        # This will definitely fail
        self.assertRaises(ValueError, content.create)

        # Check the contraints for the type container
        self.assertRaises(ValueError, content.create, type='Document', id='test-doc')

        # Check the contraints for the type parameter
        container = mock.Mock()
        self.assertRaises(ValueError, content.create, container=container, id='test-doc')

        # Check the contraints for id and title parameters
        self.assertRaises(ValueError, content.create, container=container, type='Document')

        # Check the contraints for the strict parameter, it required the id parameter
        self.assertRaises(
            ValueError, content.create,
            container=container, type='Document', strict=True, title='Spam')

    def test_create_strict(self):
        """" Test the content creating with the strict parameter. When using strict the given id
        is enforced when adding content.
        """
        container = self.portal

        # Create a page with strict option
        page = content.create(container=container, type='Document', id='strict-document', strict=True)

        assert page
        self.assertEqual(page.id, 'strict-document')
        self.assertEqual(page.portal_type, 'Document')

        # Try to create another page, this should fail
        self.assertRaises(
            BadRequest, content.create,
            container=container, type='Document', id='strict-document', strict=True
        )

    def test_create(self):
        """ Test creating content """

        container = self.portal

        folder = content.create(container=container, type='Folder', id='test-folder')
        assert folder
        self.assertEqual(folder.id, 'test-folder')
        self.assertEqual(folder.portal_type, 'Folder')

        page = content.create(container=folder, type='Document', id='test-document')
        assert page
        self.assertEqual(page.id, 'test-document')
        self.assertEqual(page.portal_type, 'Document')

    def test_get_contraints(self):
        """ Test the contraints when content is fetched with get """

        # Path and UID parameter can not be given together
        self.assertRaises(ValueError, content.get, path='/', UID='dummy')

        # Either a path or UID must be given
        self.assertRaises(ValueError, content.get)

    def test_get(self):
        """ Test the getting of content. Create a simple structure with a folder which
        contains a document
        """

        site = self.portal
        about, team = self.about, self.team

        # Test getting the about folder by path and UID
        about_by_path = content.get('/about')
        about_by_uid = content.get(UID=about.UID())
        self.assertEqual(about, about_by_path)
        self.assertEqual(about, about_by_uid)

        # Test getting the team document by path and UID
        team_by_path = content.get('/about/team')
        team_by_uid = content.get(UID=team.UID())
        self.assertEqual(team, team_by_path)
        self.assertEqual(team, team_by_uid)

        # Test getting the team document by path that has portal id included
        team_by_path = content.get('/{0}/about/team'.format(site.getId()))
        self.assertEqual(team, team_by_path)

        # Test getting an non-existing item by path and UID
        self.assertRaises(KeyError, content.get, '/spam/ham')  # restrictedTraverse raises key error
        self.assertFalse(content.get(UID='bacon'))  # Resolve by UID returns None

    def test_move_contraints(self):
        """ Test the contrains for moving content """

        # When no parameters are given an error is raised
        self.assertRaises(ValueError, content.move)

        container = mock.Mock()
        # Source is missing an should raise an error
        self.assertRaises(ValueError, content.move, source=container)
        # Target is missing an should raise an error
        self.assertRaises(ValueError, content.move, target=container)

    def test_move(self):
        """ Test moving of content """

        site = self.portal
        welcome, about, team = self.welcome, self.about, self.team

        # Move team page to portal root
        content.move(source=team, target=site)
        assert site['team']  # Content has moved to portal root
        self.assertRaises(KeyError, site['about']['team'])  # No more team in the about folder

        # When moving objects we can change the id
        content.move(source=team, target=about, id='our-team')
        assert content.get('/about/our-team')  # Content has moved to about folder
        self.assertRaises(KeyError, site['team'])  # No more team in portal root

        # Test the strict parameter when moving content
        content.move(source=welcome, target=team, id='welcome-to-about', strict=True)
        assert content.get('/about/welcome-to-about')  # Content has moved to about folder with a new id
        self.assertRaises(KeyError, site['welcome'])  # No more welcome in portal root

    def test_copy_contraints(self):

        # When no parameters are given an error is raised
        self.assertRaises(ValueError, content.copy)

        container = mock.Mock()
        # Source is missing an should raise an error
        self.assertRaises(ValueError, content.copy, source=container)
        # Target is missing an should raise an error
        self.assertRaises(ValueError, content.copy, target=container)


    def test_delete(self):
        pass

    def test_get_state(self):
        pass

    def test_transistion(self):
        pass
