# -*- coding: utf-8 -*-
"""Tests for plone.api content."""
import mock
import unittest
from zExceptions import BadRequest

from plone.api import content

class TestPloneApiContent(unittest.TestCase):
    """Unit test on IWWBSearcher using mocked service results."""

    def test_create_contraints(self):
        """ Test the contrainst when creating content """

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

        container = mock.MagicMock()
#        container.invokeFactory.return_value = 'foo'

        # Create a page with strict option
        page = content.create(container=container, type='Page', id='strict-page', strict=True)

        # Check the calls done on the mock container
        container.invokeFactory.assert_called_with('Page', 'strict-page')
        container.__getitem__.assert_called_with('strict-page')
        self.assertEqual(len(container.mock_calls), 3)


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
