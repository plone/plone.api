# -*- coding: utf-8 -*-
"""Tests for plone.api.content."""

from plone import api
from plone.api.tests.base import INTEGRATION_TESTING
from plone.api.folder import list_objects

import unittest2 as unittest


class TestPloneApiFolder(unittest.TestCase):
    """Unit tests for content manipulation using plone.api"""

    layer = INTEGRATION_TESTING

    def setUp(self):
        """Create a portal structure which we can test against.

        Plone (portal root)
        |-- blog
        |-- about
        |   |-- team
        |   `-- contact
        `-- events
            |-- training
            |-- conference
            `-- sprint
        """
        self.portal = self.layer['portal']

        self.blog = api.content.create(
            type='Link', id='blog', container=self.portal)
        self.about = api.content.create(
            type='Folder', id='about', container=self.portal)
        self.events = api.content.create(
            type='Folder', id='events', container=self.portal)

        self.team = api.content.create(
            container=self.about, type='Document', id='team')
        self.contact = api.content.create(
            container=self.about, type='Document', id='contact')

        self.training = api.content.create(
            container=self.events, type='Event', id='training')
        self.conference = api.content.create(
            container=self.events, type='Event', id='conference')
        self.sprint = api.content.create(
            container=self.events, type='Event', id='sprint')

    def test_list_objects(self):
        """Test the constraints when creating content."""

        objs = list_objects(container=self.portal)
        obj_ids = set(obj.getId() for obj in objs)
        self.assertEqual(obj_ids, {'about', 'events', 'blog'})

        objs = list_objects(container=self.portal.about)
        obj_ids = set(obj.getId() for obj in objs)
        self.assertEqual(obj_ids, {'team', 'contact'})

        objs = list_objects(container=self.portal.events)
        obj_ids = set(obj.getId() for obj in objs)
        self.assertEqual(obj_ids, {'training', 'conference', 'sprint'})

    def test_list_objects_strict(self):
        """Test with content filter checks."""
        with self.assertRaises(ValueError):
            list_objects(
                container=self.portal,
                content_filter={'no_such_index': 'foo'},
                strict=True)

    def test_list_objects_not_strict(self):
        """Test without content filter checks."""

        result = list_objects(
            container=self.portal,
            content_filter={'no_such_index': 'foo'},
            strict=False)
        self.assertEqual(len(result), 3)
