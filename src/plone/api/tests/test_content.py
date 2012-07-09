# -*- coding: utf-8 -*-
"""Tests for plone.api content."""
import mock
import unittest

from plone.api import content

class TestPloneApiContent(unittest.TestCase):
    """Unit test on IWWBSearcher using mocked service results."""

    def test_create_contraints(self):
        """ Test content creation """

        # This will definitely fail
        self.assertRaises(ValueError, content.create)

        # Now we pass type and id but leave out the container parameter
        self.assertRaises(ValueError, content.create, type='Document', id='test-doc')

        # Now we pass container and id but leave out the type parameter
        container = mock.Mock()
        self.assertRaises(ValueError, content.create, container=container, id='test-doc')

        # Now check the contraints for id and title
        self.assertRaises(ValueError, content.create, container=container, type='Document')




    def test_get(self):
        pass

    def test_move(self):
        pass

    def test_copy(self):
        pass

    def test_delete(self):
        pass

    def test_get_state(self):
        pass

    def test_transistion(self):
        pass
