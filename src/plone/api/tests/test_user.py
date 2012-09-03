# -*- coding: utf-8 -*-
"""Tests for plone.api user manipulation."""

import unittest
import mock
from Products.CMFCore.utils import getToolByName

from plone import api
from plone.api.tests.base import INTEGRATION_TESTING
from plone.app.testing import logout
from plone.app.testing import TEST_USER_NAME


class TestPloneApiUser(unittest.TestCase):
    """Test plone.api.user"""

    layer = INTEGRATION_TESTING

    def setUp(self):
        self.portal = self.layer['portal']
        self.portal_membership = getToolByName(
            self.portal, 'portal_membership')

    def test_create_no_email(self):
        """ Test that exception is raised if no email is given """

        self.portal.portal_properties.site_properties.use_email_as_login = True

        self.assertRaises(
            ValueError,
            api.user.create,
            username='chuck', password='secret'
        )

    def test_create_email_in_properties(self):
        """ Test that email is parsed from the properties """
        user = api.user.create(
            username='chuck',
            password='secret',
            properties={'email': 'chuck@norris.org'}
        )

        self.assertEquals(user.getProperty('email'), 'chuck@norris.org')

    def test_create_no_username(self):
        """ Test create if no username is provided """

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
            ValueError,
            api.user.create,
            email='chuck@norris.org', password='secret'
        )

    def test_create_with_username(self):
        """ Test if the correct username if used """
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

    def test_create_roles_set(self):
        """ Test if user has the right roles set """
        user = api.user.create(
            username='chuck',
            email='chuck@norris.org',
            password='secret',
            roles=['Reviewer', 'Editor']
        )
        self.assertEquals(
            user.getRoles(),
            ['Reviewer', 'Authenticated', 'Editor']
        )

    def test_get_constraints(self):
        """ Test that exception is raised if no username is given
        when getting the user
        """
        self.assertRaises(
            ValueError,
            api.user.get
        )

    def test_get(self):
        """ Test getting the user """
        user = api.user.create(
            username='chuck',
            email='chuck@norris.org',
            password='secret',
        )

        self.assertEqual(api.user.get('chuck'), user)

    def test_get_current(self):
        """ Test getting the currently logged-in user """
        self.assertEqual(api.user.get_current().getUserName(), TEST_USER_NAME)

    def test_get_all_users(self):
        """ Test getting all users """
        api.user.create(
            username='chuck',
            email='chuck@norris.org',
            password='secret',
        )
        users = [user.getUserName() for user in api.user.get_users()]

        self.assertEqual(users, ['chuck', TEST_USER_NAME])

    def test_get_groups_users(self):
        """ Test getting all users of a certain group """
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
        """ Test deleting of a member with email login"""

        self.portal.portal_properties.site_properties.use_email_as_login = True

        # This should fail either an username or user object should be given
        self.assertRaises(ValueError, api.user.delete)
        self.assertRaises(ValueError, api.user.delete,
                          username='chuck@norris.org', user=mock.Mock())

        api.user.create(email='chuck@norris.org', password='secret')
        api.user.delete(username='unwanted@norris.org')

        user = api.user.create(email='steven@seagal.org', password='secret')
        api.user.delete(user=user)

    def test_delete_username(self):
        """ test whether the user has been deleted """

        api.user.create(username='unwanted', password='secret',
                        email='unwanted@example.org')
        api.user.delete(username='unwanted')

        user = api.user.create(username='steven', password='secret',
                               email='steven@example.org')
        api.user.delete(user=user)

    def test_is_anonymous(self):
        """ Test anonymous access """

        self.assertEqual(api.user.is_anonymous(), False)
        logout()
        self.assertEqual(api.user.is_anonymous(), True)
