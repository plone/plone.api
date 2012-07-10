# -*- coding: utf-8 -*-
"""Tests for plone.api group."""
import mock
import unittest

from Products.CMFCore.utils import getToolByName

from plone import api
from plone.api.tests.base import INTEGRATION_TESTING


class TestPloneApiGroup(unittest.TestCase):
    """Unit tests for group manipulation using plone.api"""

    layer = INTEGRATION_TESTING

    def setUp(self):
        """  """
        self.portal = self.layer['portal']
        self.group_tool = getToolByName(self.portal, 'portal_groups')

    def test_create_contraints(self):
        """ Test the contraints for creating a group """
        self.assertRaises(ValueError, api.group.create)

    def test_create(self):
        """ Test adding of a group, groupname is mandatory """

        api.group.create(groupname='spam')
        assert self.group_tool.getGroupById('spam')

        # Group with title and description
        api.group.create(groupname='bacon', title='Bacon', description='Hmm bacon good!')
        bacon_group = self.group_tool.getGroupById('bacon')
        self.assertEqual(bacon_group.getGroupTitleOrName(), 'Bacon')
        self.assertEqual(bacon_group.getProperty('description'), 'Hmm bacon good!')

        # Group with roles and groups
        api.group.create(groupname='ham', roles=['Editor',], groups=['Reviewer',])
        ham_group = self.group_tool.getGroupById('ham')
        assert 'Editor' in ham_group.getRoles()
        assert 'Reviewer' in ham_group.getMemberIds()

    def test_get(self):
        """ Test adding of a group """

        # Create a group and retrieve it
        api.group.create(groupname='bacon')
        bacon = api.group.get(groupname='bacon')
        self.assertEqual(bacon, self.group_tool.getGroupById('bacon'))

    def test_get_all(self):
        """ Test adding of a group """

        groups = self.group_tool.listGroups()
        self.assertEqual(len(groups), 4)

    def test_delete_contraints(self):
        """ Test the contraints for deleting a group """

        # Delete group needs a groupname or group object
        self.assertRaises(ValueError, api.group.delete)

        # groupname and group are mutually exclusive
        bacon_mock = mock.Mock()
        self.assertRaises(ValueError, api.group.delete, groupname='bacon', group=bacon_mock)

    def test_delete(self):
        """ Test adding of a group """

        api.group.create(groupname='bacon')
        assert api.group.get('bacon')
        api.group.delete('bacon')
        assert not api.group.get('bacon')

