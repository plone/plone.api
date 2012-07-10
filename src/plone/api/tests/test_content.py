# -*- coding: utf-8 -*-
"""Tests for plone.api content."""
import mock
import unittest
from zExceptions import BadRequest

from plone.api import content
from plone.api.tests.base import INTEGRATION_TESTING


class TestPloneApiContent(unittest.TestCase):
    """Unit tests for content manipulation using plone.api"""

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

        self.welcome = content.create(type='Document', id='welcome', container=self.portal)
        self.about = content.create(type='Folder', id='about', container=self.portal)
        self.events = content.create(type='Folder', id='events', container=self.portal)

        self.team = content.create(container=self.about, type='Document', id='team')
        self.contact = content.create(container=self.about, type='Document', id='contact')

        self.training = content.create(container=self.events, type='Event', id='training')
        self.conference = content.create(container=self.events, type='Event', id='conference')
        self.sprint = content.create(container=self.events, type='Event', id='sprint')

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

        # Try to create another page, this should fail because of strict mode
        self.assertRaises(
            BadRequest, content.create,
            container=folder, type='Document', id='test-document'
        )

    def test_create_non_strict(self):
        """" Test the content creating without strict mode. """
        container = self.portal

        first_page = content.create(container=container, type='Document', id='test-document', strict=False)
        assert first_page
        self.assertEqual(first_page.id, 'test-document')
        self.assertEqual(first_page.portal_type, 'Document')

        # Second page is created with non-conflicting id
        second_page = content.create(container=container, type='Document', id='test-document', strict=False)
        assert second_page
        self.assertEqual(second_page.id, 'test-document-1')
        self.assertEqual(second_page.portal_type, 'Document')

    def test_get_constraints(self):
        """ Test the constraints when content is fetched with get """

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
        self.assertRaises(KeyError, content.get, '/spam/ham')
        self.assertFalse(content.get(UID='bacon'))

    def test_move_constraints(self):
        """ Test the constraints for moving content """

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
        welcome, about, team, sprint = self.welcome, self.about, self.team, self.sprint

        # Move team page to portal root
        content.move(source=team, target=site)
        assert site['team']
        assert 'team' not in site['about'].keys()

        # When moving objects we can change the id
        team = site['team']
        content.move(source=team, target=about, id='our-team')
        assert site['about']['our-team']
        assert 'team' not in site.keys()

        # Test with strict parameter disabled when moving content
        content.create(container=about, type='Document', id='welcome-to-about')
        content.move(source=welcome, target=about, id='welcome-to-about', strict=False)
        assert site['about']['welcome-to-about-1']
        assert 'welcome-to-about' not in site.keys()

    def test_copy_constraints(self):
        """ Test the constraints for moving content """

        # When no parameters are given an error is raised
        self.assertRaises(ValueError, content.copy)

        container = mock.Mock()
        # Source is missing an should raise an error
        self.assertRaises(ValueError, content.copy, source=container)
        # Target is missing an should raise an error
        self.assertRaises(ValueError, content.copy, target=container)

    def test_copy(self):
        """ Test the copying of content """

        site = self.portal
        welcome, about, team = self.welcome, self.about, self.team

        # Copy team page to portal root
        content.copy(source=team, target=site)
        assert site['team']  # Content has moved to portal root
        self.assertRaises(KeyError, site['about']['team'])

        # When moving objects we can change the id
        content.copy(source=team, target=about, id='our-team')
        assert site['about']['our-team']
        self.assertRaises(KeyError, site['team'])

        # Test the strict parameter disabled when moving content
        content.create(container=about, type='Document', id='welcome-to-about')

        content.copy(source=welcome, target=about, id='welcome-to-about', strict=False)
        assert site['about']['welcome-to-about-1']
        self.assertRaises(KeyError, site['welcome'])

    def test_delete_constraints(self):
        """ Test the constraints for deleting content """

        # When no parameters are given an error is raised
        self.assertRaises(ValueError, content.delete)

    def test_delete(self):
        """ Test deleting a content item """

        site = self.portal

        # The content item must be given as parameter
        self.assertRaises(ValueError, content.delete)

        # Delete the contact page
        content.delete(self.contact)
        assert 'contact' not in site['about'].keys()

    def test_get_state(self):
        """ Test retrieving the workflow state of a content item """

        review_state = content.get_state(obj=self.welcome)
        self.assertEqual(review_state, 'private')

    def test_transition(self):
        """ Test transitioning the workflow state on a content item"""

        content.transition(obj=self.welcome, transition='publish')
        review_state = content.get_state(obj=self.welcome)
        self.assertEqual(review_state, 'published')
