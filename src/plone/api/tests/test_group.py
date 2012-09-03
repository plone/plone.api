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
        self.portal_membership = getToolByName(
            self.portal, 'portal_membership')

    def test_create_contraints(self):
        """ Test the contraints for creating a group """
        self.assertRaises(ValueError, api.group.create)

    def test_create(self):
        """ Test adding of a group, groupname is mandatory """

        api.group.create(groupname='spam')
        assert self.group_tool.getGroupById('spam')

        # Group with title and description
        bacon_group = api.group.create(
            groupname='bacon',
            title='Bacon',
            description='Hmm bacon good!'
        )

        self.assertEqual(
            bacon_group,
            self.group_tool.getGroupById('bacon')
        )
        self.assertEqual(
            bacon_group.getGroupTitleOrName(),
            'Bacon'
        )
        self.assertEqual(
            bacon_group.getProperty('description'),
            'Hmm bacon good!'
        )

        # Group with roles and groups
        ham_group = api.group.create(
            groupname='ham',
            roles=['Editor', ],
            groups=['Reviewer', ]
        )
        group = self.group_tool.getGroupById('ham')
        self.assertEqual(ham_group, group)
        assert 'Editor' in ham_group.getRoles()
        assert 'Reviewer' in ham_group.getMemberIds()

    def test_get_constraints(self):
        """ Test the constraints for geting a group """
        self.assertRaises(ValueError, api.group.get)

    def test_get(self):
        """ Test getting a group """

        # This should fail because the groupname is mandatory
        self.assertRaises(ValueError, api.group.create)

        # Create a group and retrieve it
        api.group.create(groupname='bacon')
        bacon = api.group.get(groupname='bacon')

        self.assertEqual(
            bacon,
            self.group_tool.getGroupById('bacon')
        )

    def test_get_all_groups(self):
        """ Test getting all groups """

        groups = api.group.get_groups()
        self.assertEqual(len(groups), 4)

    def test_get_groups_constraints(self):
        """ Test that exception is raised if wrong arguments are given """

        # username and user are mutually exclusive
        user = mock.Mock()
        # user = api.user.create(
        #     username='chuck',
        #     email='chuck@norris.org',
        #     password='secret'
        # )
        self.assertRaises(
            ValueError,
            api.group.get_groups,
            username='chuck', user=user,
        )

    def test_get_users_groups(self):
        """ Test retrieving of groups that the user is member of. """
        user = self.portal_membership.getAuthenticatedMember()

        api.group.create(groupname='staff')
        api.group.add_user(groupname='staff', user=user)

        groups = [g.id for g in api.group.get_groups(user=user)]
        assert 'AuthenticatedUsers' in groups
        assert 'staff' in groups

        groups = [g.id for g in api.group.get_groups(username=user.id)]
        assert 'AuthenticatedUsers' in groups
        assert 'staff' in groups

    def test_delete_contraints(self):
        """ Test the contraints for deleting a group """

        # Delete group needs a groupname or group object
        self.assertRaises(ValueError, api.group.delete)

        # groupname and group are mutually exclusive
        bacon_mock = mock.Mock()
        self.assertRaises(
            ValueError,
            api.group.delete,
            groupname='bacon',
            group=bacon_mock
        )

    def test_delete(self):
        """ Test deleting a group """

        # Test deleting a group by passing in a groupname
        api.group.create(groupname='bacon')
        assert api.group.get('bacon')

        api.group.delete(groupname='bacon')
        assert not api.group.get('bacon')

        # Test deleting a group by passing in a group object
        group = api.group.create(groupname='bacon')
        assert api.group.get('bacon')

        api.group.delete(group=group)
        assert not api.group.get('bacon')

    def test_add_user_contraints(self):
        """ Test the constraints when a user is added to a group """

        group, user = mock.Mock(), mock.Mock()

        # Arguments ``groupname`` and ``group`` are also mutually exclusive.
        self.assertRaises(
            ValueError,
            api.group.add_user,
            groupname='staff', group=group
        )
        # Arguments ``username`` and ``user`` are mutually exclusive.
        self.assertRaises(
            ValueError,
            api.group.add_user,
            username='staff', user=user
        )
        self.assertRaises(ValueError, api.group.add_user, groupname='staff')
        self.assertRaises(ValueError, api.group.add_user, username='jane')
        self.assertRaises(
            ValueError,
            api.group.add_user,
            username='jane',
            group='group',
            groupname='staff'
        )

    def test_add_user(self):
        """ Test adding a user to a group """

        api.group.create(groupname='staff')
        api.user.create(email='jane@plone.org', username='jane')
        api.user.create(email='bob@plone.org', username='bob')

        # Add user by username to group
        api.group.add_user(groupname='staff', username='bob')

        # Add user by user object to group
        user = api.user.get(username='jane')
        group = api.group.get(groupname='staff')
        api.group.add_user(group=group, user=user)

        assert 'staff' in [g.id for g in api.group.get_groups(username='bob')]
        assert 'staff' in [g.id for g in api.group.get_groups(username='jane')]

        assert 'bob' in group.getMemberIds()
        assert 'jane' in group.getMemberIds()

    def test_remove_user_contraints(self):
        """ Test the constraints when a user is removed from a group """

        group, user = mock.Mock(), mock.Mock()

        # Arguments ``groupname`` and ``group`` are also mutually exclusive.
        self.assertRaises(
            ValueError,
            api.group.remove_user,
            groupname='staff', group=group
        )
        # Arguments ``username`` and ``user`` are mutually exclusive.
        self.assertRaises(
            ValueError,
            api.group.remove_user,
            username='staff', user=user
        )
        self.assertRaises(ValueError, api.group.remove_user, groupname='staff')
        self.assertRaises(ValueError, api.group.remove_user, username='jane')
        self.assertRaises(
            ValueError,
            api.group.remove_user,
            username='jane',
            group='group',
            groupname='staff'
        )

    def test_remove_user(self):
        """ Test removing a user from a group """

        api.group.create(groupname='staff')
        api.user.create(email='jane@plone.org', username='jane')
        api.user.create(email='bob@plone.org', username='bob')
        api.group.add_user(groupname='staff', username='jane')
        api.group.add_user(groupname='staff', username='bob')

        # Delete user by username from group
        api.group.remove_user(groupname='staff', username='bob')

        group = api.group.get(groupname='staff')
        user = api.user.get(username='jane')

        # Delete user by user object from group
        api.group.remove_user(group=group, user=user)

        assert 'staff' not in api.group.get_groups(username='bob')
        assert 'staff' not in api.group.get_groups(username='jane')

        assert 'bob' not in group.getMemberIds()
        assert 'jane' not in group.getMemberIds()
