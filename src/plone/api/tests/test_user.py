# -*- coding: utf-8 -*-
"""Tests for plone.api.user."""

from plone import api
from plone.api.exc import InvalidParameterError
from plone.api.exc import MissingParameterError
from plone.api.tests.base import INTEGRATION_TESTING
from plone.app.testing import logout
from plone.app.testing import TEST_USER_NAME
from Products.CMFCore.utils import getToolByName

import mock
import unittest2 as unittest


class TestPloneApiUser(unittest.TestCase):
    """Test plone.api.user."""

    layer = INTEGRATION_TESTING

    def setUp(self):
        """Shared test environment set-up, ran before every test."""
        self.portal = self.layer['portal']
        self.portal_membership = getToolByName(
            self.portal, 'portal_membership')

    def test_create_no_email(self):
        """Test that exception is raised if no email is given."""

        self.portal.portal_properties.site_properties.use_email_as_login = True

        self.assertRaises(
            MissingParameterError,
            api.user.create,
            username='chuck', password='secret'
        )

    def test_create_email_in_properties(self):
        """Test that email is parsed from the properties."""
        user = api.user.create(
            username='chuck',
            password='secret',
            properties={'email': 'chuck@norris.org'}
        )

        self.assertEquals(user.getProperty('email'), 'chuck@norris.org')

    def test_create_no_username(self):
        """Test create if no username is provided."""

        # If there is no username, email will be used instead
        properties = self.portal.portal_properties.site_properties
        properties.manage_changeProperties(use_email_as_login=True)

        user = api.user.create(
            email='chuck@norris.org',
            password='secret'
        )

        self.assertEquals(user.getUserName(), 'chuck@norris.org')

        # But if using emails as a username is disabled, we should get
        # an error
        properties.manage_changeProperties(use_email_as_login=False)

        self.assertRaises(
            InvalidParameterError,
            api.user.create,
            email='chuck@norris.org', password='secret'
        )

    def test_create_with_username(self):
        """Test if the correct username if used."""
        properties = self.portal.portal_properties.site_properties
        properties.manage_changeProperties(use_email_as_login=True)

        user = api.user.create(
            username='chuck',
            email='chuck@norris.org',
            password='secret',
        )
        self.assertEquals(user.getUserName(), 'chuck@norris.org')

        properties = self.portal.portal_properties.site_properties
        properties.manage_changeProperties(use_email_as_login=False)

        user = api.user.create(
            username='chuck',
            email='chuck@norris.org',
            password='secret',
        )
        self.assertEquals(user.getUserName(), 'chuck')

    def test_create_default_roles(self):
        """Test the default role is set to member."""
        # if create is given no roles, member is the default
        user = api.user.create(
            username='chuck',
            email='chuck@norris.org',
            password='secret',
        )
        self.assertEquals(
            api.user.get_roles(user=user),
            ['Member', 'Authenticated', ]
        )

    def test_create_specified_roles(self):
        """Test specific roles are set correctly."""
        user = api.user.create(
            username='chuck',
            email='chuck@norris.org',
            password='secret',
            roles=['Reviewer', 'Editor']
        )
        self.assertEquals(
            api.user.get_roles(user=user),
            ['Reviewer', 'Authenticated', 'Editor']
        )

    def test_create_no_roles(self):
        """Test that passing an empty list give a user with no member role."""
        user = api.user.create(
            username='chuck',
            email='chuck@norris.org',
            password='secret',
            roles=[]
        )
        self.assertEquals(
            api.user.get_roles(user=user),
            ['Authenticated', ]
        )

    def test_get_constraints(self):
        """Test that exception is raised if no username is given when getting
        the user.

        """
        self.assertRaises(
            MissingParameterError,
            api.user.get
        )

    def test_get(self):
        """Test getting the user."""
        user = api.user.create(
            username='chuck',
            email='chuck@norris.org',
            password='secret',
        )

        self.assertEqual(api.user.get('chuck'), user)

    def test_get_current(self):
        """Test getting the currently logged-in user."""
        self.assertEqual(api.user.get_current().getUserName(), TEST_USER_NAME)

    def test_get_all_users(self):
        """Test getting all users."""
        api.user.create(
            username='chuck',
            email='chuck@norris.org',
            password='secret',
        )
        users = [user.getUserName() for user in api.user.get_users()]

        self.assertEqual(users, ['chuck', TEST_USER_NAME])

    def test_get_groups_users(self):
        """Test getting all users of a certain group."""
        api.user.create(
            username='chuck',
            email='chuck@norris.org',
            password='secret',
        )
        api.group.create(groupname='staff')
        api.group.add_user(username='chuck', groupname='staff')

        users = api.user.get_users(groupname='staff')
        usernames = [user.getUserName() for user in users]

        self.assertEqual(usernames, ['chuck'])

    def test_delete_no_username(self):
        """Test deleting of a member with email login."""

        self.portal.portal_properties.site_properties.use_email_as_login = True

        # This should fail either an username or user object should be given
        self.assertRaises(MissingParameterError, api.user.delete)
        self.assertRaises(InvalidParameterError, api.user.delete,
                          username='chuck@norris.org', user=mock.Mock())

        api.user.create(email='chuck@norris.org', password='secret')
        api.user.delete(username='unwanted@norris.org')

        user = api.user.create(email='steven@seagal.org', password='secret')
        api.user.delete(user=user)

    def test_delete_username(self):
        """test whether the user has been deleted."""

        api.user.create(username='unwanted', password='secret',
                        email='unwanted@example.org')
        api.user.delete(username='unwanted')

        user = api.user.create(username='steven', password='secret',
                               email='steven@example.org')
        api.user.delete(user=user)

    def test_is_anonymous(self):
        """Test anonymous access."""

        self.assertEqual(api.user.is_anonymous(), False)
        logout()
        self.assertEqual(api.user.is_anonymous(), True)

    def test_get_roles(self):
        """Test get roles."""

        ROLES = ['Reviewer', 'Editor']
        user = api.user.create(
            username='chuck',
            email='chuck@norris.org',
            password='secret',
            roles=ROLES
        )
        ROLES = set(ROLES + ['Authenticated'])
        self.assertEqual(ROLES, set(api.user.get_roles(username='chuck')))
        self.assertEqual(ROLES, set(api.user.get_roles(user=user)))

        self.assertRaises(
            InvalidParameterError,
            api.user.get_roles,
            username='chuck',
            user=user)

    def test_get_permissions_root(self):
        """ Test get permissions on site root"""

        user = api.user.create(
            username='chuck',
            email='chuck@norris.org',
            password='secret',
            roles=[]
        )

        self.assertRaises(
            InvalidParameterError,
            api.user.get_permissions,
            username='chuck',
            user=user)

        PERMISSIONS = {
            'View': True,
            'Manage portal': False,
            'Modify portal content': False,
            'Access contents information': True,
        }

        for k, v in PERMISSIONS.items():
            self.assertEqual(v,
                             api.user.get_permissions(username='chuck').get(k, None))
            self.assertEqual(v,
                             api.user.get_permissions(user=user).get(k, None))

    def test_get_permissions_context(self):
        """ Test get permissions on some context"""

        user = api.user.create(
            username='chuck',
            email='chuck@norris.org',
            password='secret',
            roles=[]
        )

        self.assertRaises(
            InvalidParameterError,
            api.user.get_permissions,
            username='chuck',
            user=user)

        PERMISSIONS = {
            'View': False,
            'Manage portal': False,
            'Modify portal content': False,
            'Access contents information': False,
        }

        folder = api.content.create(
            container=self.portal,
            type='Folder',
            id='folder_one',
            title='Folder One')

        for k, v in PERMISSIONS.items():
            self.assertEqual(v,
                             api.user.get_permissions(
                                 username='chuck',
                                 obj=folder).get(k, None))
            self.assertEqual(v,
                             api.user.get_permissions(
                                 user=user,
                                 obj=folder).get(k, None))

    def test_grant_roles(self):
        """Test grant roles."""

        user = api.user.create(
            username='chuck',
            email='chuck@norris.org',
            password='secret',
        )

        self.assertRaises(
            InvalidParameterError,
            api.user.grant_roles,
            username='chuck',
            roles=['Anonymous'])

        self.assertRaises(
            InvalidParameterError,
            api.user.grant_roles,
            username='chuck',
            roles=['Authenticated'])

        self.assertRaises(
            InvalidParameterError,
            api.user.grant_roles,
            username='chuck',
            user=user)

        api.user.grant_roles(username='chuck', roles=['Editor'])
        self.assertIn('Editor', api.user.get_roles(username='chuck'))
        self.assertIn('Editor', api.user.get_roles(user=user))

        api.user.grant_roles(username='chuck', roles=('Contributor',))
        self.assertIn('Contributor', api.user.get_roles(username='chuck'))
        self.assertIn('Contributor', api.user.get_roles(user=user))

        api.user.grant_roles(username='chuck', roles=['Reader', 'Reader'])
        ROLES = {'Editor', 'Contributor', 'Reader', 'Authenticated', 'Member'}
        self.assertEqual(ROLES, set(api.user.get_roles(username='chuck')))
        self.assertEqual(ROLES, set(api.user.get_roles(user=user)))

    def test_revoke_roles(self):
        """Test revoke roles."""

        user = api.user.create(
            username='chuck',
            email='chuck@norris.org',
            password='secret',
        )

        self.assertRaises(
            InvalidParameterError,
            api.user.grant_roles,
            username='chuck',
            roles=['Anonymous'])

        self.assertRaises(
            InvalidParameterError,
            api.user.grant_roles,
            username='chuck',
            roles=['Authenticated'])

        self.assertRaises(
            InvalidParameterError,
            api.user.grant_roles,
            username='chuck',
            user=user)

        api.user.grant_roles(username='chuck', roles=['Reviewer', 'Editor'])

        api.user.revoke_roles(username='chuck', roles=['Reviewer'])
        self.assertNotIn('Reviewer', api.user.get_roles(username='chuck'))
        self.assertNotIn('Reviewer', api.user.get_roles(user=user))
        self.assertIn('Editor', api.user.get_roles(username='chuck'))
        self.assertIn('Editor', api.user.get_roles(user=user))

        api.user.revoke_roles(username='chuck', roles=['Editor'])
        ROLES = {'Authenticated', 'Member'}
        self.assertEqual(ROLES, set(api.user.get_roles(username='chuck')))
        self.assertEqual(ROLES, set(api.user.get_roles(user=user)))

    def test_grant_roles_in_context(self):
        """Test grant roles."""

        user = api.user.create(
            username='chuck',
            email='chuck@norris.org',
            password='secret',
        )

        portal = api.portal.get()
        folder = api.content.create(
            container=portal,
            type='Folder',
            id='folder_one',
            title='Folder One')
        document = api.content.create(
            container=folder,
            type='Document',
            id='document_one',
            title='Document One')

        api.user.grant_roles(username='chuck', roles=['Editor'], obj=folder)
        self.assertIn('Editor', api.user.get_roles(username='chuck', obj=folder))
        self.assertIn('Editor', api.user.get_roles(user=user, obj=folder))
        self.assertIn('Editor', api.user.get_roles(username='chuck', obj=document))
        self.assertIn('Editor', api.user.get_roles(user=user, obj=document))

        api.user.grant_roles(username='chuck', roles=('Contributor',), obj=folder)
        self.assertIn('Contributor', api.user.get_roles(username='chuck', obj=folder))
        self.assertIn('Contributor', api.user.get_roles(user=user, obj=folder))
        self.assertIn('Contributor', api.user.get_roles(username='chuck', obj=document))
        self.assertIn('Contributor', api.user.get_roles(user=user, obj=document))

        ROLES = {'Editor', 'Contributor', 'Authenticated', 'Member'}
        self.assertEqual(ROLES, set(api.user.get_roles(username='chuck', obj=folder)))
        self.assertEqual(ROLES, set(api.user.get_roles(user=user, obj=folder)))
        self.assertEqual(ROLES, set(api.user.get_roles(username='chuck', obj=document)))
        self.assertEqual(ROLES, set(api.user.get_roles(user=user, obj=document)))

    def test_revoke_roles_in_context(self):
        """Test revoke roles."""

        user = api.user.create(
            username='chuck',
            email='chuck@norris.org',
            password='secret',
        )

        portal = api.portal.get()
        folder = api.content.create(container=portal,
                                    type='Folder',
                                    id='folder_one',
                                    title='Folder One')
        document = api.content.create(container=folder,
                                      type='Document',
                                      id='document_one',
                                      title='Document One')
        api.user.grant_roles(username='chuck',
                             roles=['Reviewer', 'Editor'],
                             obj=folder)

        api.user.revoke_roles(username='chuck', roles=['Reviewer'], obj=folder)
        self.assertIn('Editor', api.user.get_roles(username='chuck', obj=folder))
        self.assertIn('Editor', api.user.get_roles(user=user, obj=folder))
        self.assertIn('Editor', api.user.get_roles(username='chuck', obj=document))
        self.assertIn('Editor', api.user.get_roles(user=user, obj=document))
        self.assertNotIn('Reviewer', api.user.get_roles(username='chuck', obj=folder))
        self.assertNotIn('Reviewer', api.user.get_roles(user=user, obj=folder))
        self.assertNotIn('Reviewer', api.user.get_roles(username='chuck', obj=document))
        self.assertNotIn('Reviewer', api.user.get_roles(user=user, obj=document))

        api.user.revoke_roles(username='chuck', roles=['Editor'], obj=folder)
        self.assertNotIn('Editor', api.user.get_roles(username='chuck', obj=folder))
        self.assertNotIn('Editor', api.user.get_roles(user=user, obj=folder))
        self.assertNotIn('Editor', api.user.get_roles(username='chuck', obj=document))
        self.assertNotIn('Editor', api.user.get_roles(user=user, obj=document))

        ROLES = {'Authenticated', 'Member'}
        self.assertEqual(ROLES, set(api.user.get_roles(username='chuck', obj=folder)))
        self.assertEqual(ROLES, set(api.user.get_roles(user=user, obj=folder)))
        self.assertEqual(ROLES, set(api.user.get_roles(username='chuck',
                                                       obj=document)))
        self.assertEqual(ROLES, set(api.user.get_roles(user=user,
                                                       obj=document)))
