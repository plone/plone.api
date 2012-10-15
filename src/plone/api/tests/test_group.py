# -*- coding: utf-8 -*-
"""Tests for plone.api.group."""

from plone import api
from plone.api.tests.base import INTEGRATION_TESTING
from Products.CMFCore.utils import getToolByName

import mock
import unittest2 as unittest


class TestPloneApiGroup(unittest.TestCase):
    """Unit tests for group manipulation using plone.api."""

    layer = INTEGRATION_TESTING

    def setUp(self):
        """Shared test environment set-up, ran before every test."""
        self.portal = self.layer['portal']
        self.group_tool = getToolByName(self.portal, 'portal_groups')
        self.portal_membership = getToolByName(
            self.portal, 'portal_membership')

    def test_create_contraints(self):
        """Test the contraints for creating a group."""
        self.assertRaises(ValueError, api.group.create)

    def test_create(self):
        """Test adding of a group, groupname is mandatory."""

        spam_group = api.group.create(groupname='spam')
        self.assertEqual(spam_group, self.group_tool.getGroupById('spam'))

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
        self.assertIn('Editor', ham_group.getRoles())
        self.assertIn('Reviewer', ham_group.getMemberIds())

    def test_get_constraints(self):
        """Test the constraints for geting a group."""
        self.assertRaises(ValueError, api.group.get)

    def test_get(self):
        """Test getting a group."""

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
        """Test getting all groups."""

        groups = api.group.get_groups()
        self.assertEqual(len(groups), 4)

    def test_get_groups_constraints(self):
        """Test that exception is raised if wrong arguments are given."""

        # username and user are mutually exclusive
        self.assertRaises(
            ValueError,
            api.group.get_groups,
            username='chuck', user=mock.Mock(),
        )

    def test_get_users_groups(self):
        """Test retrieving of groups that the user is member of."""
        user = self.portal_membership.getAuthenticatedMember()

        api.group.create(groupname='staff')
        api.group.add_user(groupname='staff', user=user)

        groups = [g.id for g in api.group.get_groups(user=user)]
        self.assertIn('AuthenticatedUsers', groups)
        self.assertIn('staff', groups)

        groups = [g.id for g in api.group.get_groups(username=user.id)]
        self.assertIn('AuthenticatedUsers', groups)
        self.assertIn('staff', groups)

        self.assertRaises(ValueError,
                          api.group.get_groups,
                          username='theurbanspaceman')

    def test_delete_contraints(self):
        """Test the contraints for deleting a group."""

        # Delete group needs a groupname or group object
        self.assertRaises(ValueError, api.group.delete)

        # groupname and group are mutually exclusive
        self.assertRaises(
            ValueError,
            api.group.delete,
            groupname='bacon',
            group=mock.Mock()
        )

    def test_delete(self):
        """Test deleting a group."""

        # Test deleting a group by passing in a groupname
        bacon = api.group.create(groupname='bacon')
        self.assertEqual(bacon, api.group.get('bacon'))

        api.group.delete(groupname='bacon')
        self.assertIsNone(api.group.get('bacon'))

        # Test deleting a group by passing in a group object
        group = api.group.create(groupname='bacon')
        self.assertEqual(group, api.group.get('bacon'))

        api.group.delete(group=group)
        self.assertIsNone(api.group.get('bacon'))

    def test_add_user_contraints(self):
        """Test the constraints when a user is added to a group."""

        # Arguments ``groupname`` and ``group`` are mutually exclusive.
        self.assertRaises(
            ValueError,
            api.group.add_user,
            groupname='staff', group=mock.Mock()
        )
        # Arguments ``username`` and ``user`` are mutually exclusive.
        self.assertRaises(
            ValueError,
            api.group.add_user,
            username='staff', user=mock.Mock()
        )
        self.assertRaises(ValueError, api.group.add_user, groupname='staff')
        self.assertRaises(ValueError, api.group.add_user, username='jane')
        self.assertRaises(
            ValueError,
            api.group.add_user,
            username='jane',
            groupname='staff',
            group=mock.Mock(),
        )

    def test_add_user(self):
        """Test adding a user to a group."""

        api.group.create(groupname='staff')
        api.user.create(email='jane@plone.org', username='jane')
        api.user.create(email='bob@plone.org', username='bob')

        # Add user by username to group
        api.group.add_user(groupname='staff', username='bob')

        # Add user by user object to group
        user = api.user.get(username='jane')
        group = api.group.get(groupname='staff')
        api.group.add_user(group=group, user=user)

        self.assertIn('staff', [g.id for g in api.group.get_groups(username='bob')])
        self.assertIn('staff', [g.id for g in api.group.get_groups(username='jane')])

        self.assertIn('bob', group.getMemberIds())
        self.assertIn('jane', group.getMemberIds())

    def test_remove_user_contraints(self):
        """Test the constraints when a user is removed from a group."""

        # Arguments ``groupname`` and ``group`` are mutually exclusive.
        self.assertRaises(
            ValueError,
            api.group.remove_user,
            groupname='staff', group=mock.Mock()
        )
        # Arguments ``username`` and ``user`` are mutually exclusive.
        self.assertRaises(
            ValueError,
            api.group.remove_user,
            username='staff', user=mock.Mock()
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
        """Test removing a user from a group."""

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

        self.assertNotIn('staff', api.group.get_groups(username='bob'))
        self.assertNotIn('staff', api.group.get_groups(username='jane'))

        self.assertNotIn('bob', group.getMemberIds())
        self.assertNotIn('jane', group.getMemberIds())

    def test_grant_roles(self):
        """Test grant roles."""

        group = api.group.create(groupname='foo')

        self.assertRaises(
            ValueError,
            api.group.grant_roles,
            groupname='foo',
            roles=['Anonymous'])

        self.assertRaises(
            ValueError,
            api.group.grant_roles,
            groupname='foo',
            roles=['Authenticated'])

        self.assertRaises(
            ValueError,
            api.group.grant_roles,
            groupname='foo',
            group=group)

        api.group.grant_roles(groupname='foo', roles=['Editor'])
        self.assertIn('Editor', api.group.get_roles(groupname='foo'))
        self.assertIn('Editor', api.group.get_roles(group=group))

        api.group.grant_roles(groupname='foo', roles=('Contributor',))
        self.assertIn('Contributor', api.group.get_roles(groupname='foo'))
        self.assertIn('Contributor', api.group.get_roles(group=group))

        api.group.grant_roles(groupname='foo', roles=['Reader', 'Reader'])
        ROLES = set(['Editor', 'Contributor', 'Reader', 'Authenticated'])
        self.assertEqual(ROLES, set(api.group.get_roles(groupname='foo')))
        self.assertEqual(ROLES, set(api.group.get_roles(group=group)))

    def test_revoke_roles(self):
        """Test revoke roles."""

        group = api.group.create(groupname='bar')

        self.assertRaises(
            ValueError,
            api.group.grant_roles,
            groupname='bar',
            roles=['Anonymous'])

        self.assertRaises(
            ValueError,
            api.group.grant_roles,
            groupname='bar',
            roles=['Authenticated'])

        self.assertRaises(
            ValueError,
            api.group.grant_roles,
            groupname='bar',
            group=group)

        api.group.grant_roles(groupname='bar', roles=['Reviewer', 'Editor'])

        api.group.revoke_roles(groupname='bar', roles=['Reviewer'])
        self.assertNotIn('Reviewer', api.group.get_roles(groupname='bar'))
        self.assertNotIn('Reviewer', api.group.get_roles(group=group))
        self.assertIn('Editor', api.group.get_roles(groupname='bar'))
        self.assertIn('Editor', api.group.get_roles(group=group))

        api.group.revoke_roles(groupname='bar', roles=['Editor'])
        ROLES = set(['Authenticated'])
        self.assertEqual(ROLES, set(api.group.get_roles(groupname='bar')))
        self.assertEqual(ROLES, set(api.group.get_roles(group=group)))

    def test_grant_roles_in_context(self):
        """Test grant roles."""

        group = api.group.create(groupname='foo')

        portal = api.portal.get()
        folder = api.content.create(container=portal, type='Folder', id='folder_one', title='Folder One')
        document = api.content.create(container=folder, type='Document', id='document_one', title='Document One')

        api.group.grant_roles(groupname='foo', roles=['Editor'], obj=folder)
        self.assertIn('Editor', api.group.get_roles(groupname='foo', obj=folder))
        self.assertIn('Editor', api.group.get_roles(group=group, obj=folder))
        self.assertIn('Editor', api.group.get_roles(groupname='foo', obj=document))
        self.assertIn('Editor', api.group.get_roles(group=group, obj=document))

        api.group.grant_roles(groupname='foo', roles=('Contributor',), obj=folder)
        self.assertIn('Contributor', api.group.get_roles(groupname='foo', obj=folder))
        self.assertIn('Contributor', api.group.get_roles(group=group, obj=folder))
        self.assertIn('Contributor', api.group.get_roles(groupname='foo', obj=document))
        self.assertIn('Contributor', api.group.get_roles(group=group, obj=document))

        ROLES = set(['Editor', 'Contributor', 'Authenticated'])
        self.assertEqual(ROLES, set(api.group.get_roles(groupname='foo', obj=folder)))
        self.assertEqual(ROLES, set(api.group.get_roles(group=group, obj=folder)))
        self.assertEqual(ROLES, set(api.group.get_roles(groupname='foo', obj=document)))
        self.assertEqual(ROLES, set(api.group.get_roles(group=group, obj=document)))

    def test_revoke_roles_in_context(self):
        """Test revoke roles."""

        group = api.group.create(groupname='ploneboat')

        portal = api.portal.get()
        folder = api.content.create(container=portal, type='Folder', id='folder_one', title='Folder One')
        document = api.content.create(container=folder, type='Document', id='document_one', title='Document One')
        api.group.grant_roles(groupname='ploneboat', roles=['Reviewer', 'Editor'], obj=folder)

        api.group.revoke_roles(groupname='ploneboat', roles=['Reviewer'], obj=folder)
        self.assertIn('Editor', api.group.get_roles(groupname='ploneboat', obj=folder))
        self.assertIn('Editor', api.group.get_roles(group=group, obj=folder))
        self.assertIn('Editor', api.group.get_roles(groupname='ploneboat', obj=document))
        self.assertIn('Editor', api.group.get_roles(group=group, obj=document))
        self.assertNotIn('Reviewer', api.group.get_roles(groupname='ploneboat', obj=folder))
        self.assertNotIn('Reviewer', api.group.get_roles(group=group, obj=folder))
        self.assertNotIn('Reviewer', api.group.get_roles(groupname='ploneboat', obj=document))
        self.assertNotIn('Reviewer', api.group.get_roles(group=group, obj=document))

        api.group.revoke_roles(groupname='ploneboat', roles=['Editor'], obj=folder)
        self.assertNotIn('Editor', api.group.get_roles(groupname='ploneboat', obj=folder))
        self.assertNotIn('Editor', api.group.get_roles(group=group, obj=folder))
        self.assertNotIn('Editor', api.group.get_roles(groupname='ploneboat', obj=document))
        self.assertNotIn('Editor', api.group.get_roles(group=group, obj=document))

        ROLES = set(['Authenticated', ])
        self.assertEqual(ROLES, set(api.group.get_roles(groupname='ploneboat', obj=folder)))
        self.assertEqual(ROLES, set(api.group.get_roles(group=group, obj=folder)))
        self.assertEqual(ROLES, set(api.group.get_roles(groupname='ploneboat', obj=document)))
        self.assertEqual(ROLES, set(api.group.get_roles(group=group, obj=document)))
