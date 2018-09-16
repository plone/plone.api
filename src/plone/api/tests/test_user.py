# -*- coding: utf-8 -*-
"""Tests for plone.api.user."""

from AccessControl.Permission import getPermissions
from borg.localrole.interfaces import ILocalRoleProvider
from plone import api
from plone.api.tests.base import INTEGRATION_TESTING
from plone.app.testing import logout
from plone.app.testing import TEST_USER_ID
from plone.app.testing import TEST_USER_NAME
from zope.component import adapter
from zope.component import getGlobalSiteManager
from zope.component import provideAdapter
from zope.interface import implementer
from zope.interface import Interface

import mock
import six
import unittest


class TestPloneApiUser(unittest.TestCase):
    """Test plone.api.user."""

    layer = INTEGRATION_TESTING

    def setUp(self):
        """Shared test environment set-up, ran before every test."""
        self.portal = self.layer['portal']
        self.portal_membership = api.portal.get_tool('portal_membership')

    def _check_userid_and_username_different(self):
        """Ensure that the userid and username are not equal

        This is important for tests which rely on differentiation between the
        two. These tests should rely on the Test User created by
        plone.app.testing, which has these conditions. If that implementation
        detail should change, any test containing a call to this method will
        be invalidated, and should fail.
        """
        user = api.user.get_current()
        userid = user.id
        username = user.getUserName()
        self.assertNotEqual(userid, username)

    def _set_emaillogin(self, value):
        from plone.api.exc import InvalidParameterError
        try:
            api.portal.set_registry_record('plone.use_email_as_login', value)
        except InvalidParameterError:
            portal = api.portal.get()
            portal.portal_properties.site_properties.use_email_as_login = value

    def test_create_no_email(self):
        """Test that exception is raised if no email is given."""

        self._set_emaillogin(True)

        from plone.api.exc import MissingParameterError
        with self.assertRaises(MissingParameterError):
            api.user.create(
                username='chuck',
                password='secret',
            )

    def test_get_user_userid_username(self):
        """Enforce user.get works with username and userid."""
        self._check_userid_and_username_different()
        self.assertEqual(
            api.user.get(userid=TEST_USER_ID).getId(),
            api.user.get_current().getId(),
        )
        self.assertEqual(
            api.user.get(username=TEST_USER_NAME).getId(),
            api.user.get_current().getId(),
        )

    def test_create_email_in_properties(self):
        """Test that email is parsed from the properties."""
        user = api.user.create(
            username='chuck',
            password='secret',
            properties={'email': 'chuck@norris.org'},
        )

        self.assertEqual(user.getProperty('email'), 'chuck@norris.org')

    def test_create_no_username(self):
        """Test create if no username is provided."""

        # If there is no username, email will be used instead
        self._set_emaillogin(True)

        user = api.user.create(
            email='chuck@norris.org',
            password='secret',
        )

        self.assertEqual(user.getUserName(), 'chuck@norris.org')

        # But if using emails as a username is disabled, we should get
        # an error
        self._set_emaillogin(False)

        from plone.api.exc import InvalidParameterError
        with self.assertRaises(InvalidParameterError):
            api.user.create(
                email='chuck@norris.org',
                password='secret',
            )

    def test_create_with_username(self):
        """Test if the correct username if used."""
        self._set_emaillogin(True)

        user = api.user.create(
            username='chuck',
            email='chuck@norris.org',
            password='secret',
        )
        self.assertEqual(user.getUserName(), 'chuck@norris.org')

        self._set_emaillogin(False)

        user = api.user.create(
            username='chuck',
            email='chuck@norris.org',
            password='secret',
        )
        self.assertEqual(user.getUserName(), 'chuck')

    def test_create_default_roles(self):
        """Test the default role is set to member."""
        # if create is given no roles, member is the default
        user = api.user.create(
            username='chuck',
            email='chuck@norris.org',
            password='secret',
        )
        if six.PY2:
            assertCountEqual = self.assertItemsEqual
        else:
            assertCountEqual = self.assertCountEqual
        assertCountEqual(
            api.user.get_roles(user=user),
            ['Member', 'Authenticated'],
        )

    def test_create_specified_roles(self):
        """Test specific roles are set correctly."""
        user = api.user.create(
            username='chuck',
            email='chuck@norris.org',
            password='secret',
            roles=['Reviewer', 'Editor'],
        )
        if six.PY2:
            assertCountEqual = self.assertItemsEqual
        else:
            assertCountEqual = self.assertCountEqual

        assertCountEqual(
            api.user.get_roles(user=user),
            ['Reviewer', 'Authenticated', 'Editor'],
        )

    def test_create_no_roles(self):
        """Test that passing an empty list give a user with no member role."""
        user = api.user.create(
            username='chuck',
            email='chuck@norris.org',
            password='secret',
            roles=[],
        )
        if six.PY2:
            assertCountEqual = self.assertItemsEqual
        else:
            assertCountEqual = self.assertCountEqual
        assertCountEqual(
            api.user.get_roles(user=user),
            ['Authenticated'],
        )

    def test_get_constraints(self):
        """Test that exception is raised if no username is given when getting
        the user.
        """
        from plone.api.exc import MissingParameterError
        with self.assertRaises(MissingParameterError):
            api.user.get()

    def test_get(self):
        """Test getting the user."""
        user = api.user.create(
            username='chuck',
            email='chuck@norris.org',
            password='secret',
        )
        self.assertEqual(api.user.get('chuck').id, user.id)

    def test_get_current(self):
        """Test getting the currently logged-in user."""
        self.assertEqual(
            api.user.get_current().getUserName(),
            TEST_USER_NAME,
        )

    def test_get_all_users(self):
        """Test getting all users."""
        api.user.create(
            username='chuck',
            email='chuck@norris.org',
            password='secret',
        )
        users = [user.getUserName() for user in api.user.get_users()]
        if six.PY2:
            assertCountEqual = self.assertItemsEqual
        else:
            assertCountEqual = self.assertCountEqual
        assertCountEqual(
            users,
            ['chuck', TEST_USER_NAME],
        )

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

    def test_get_users_groupname_and_group(self):
        """Test getting users passing both groupname and group."""
        api.group.create(groupname='bacon')
        bacon = api.group.get(groupname='bacon')

        from plone.api.exc import InvalidParameterError
        with self.assertRaises(InvalidParameterError):
            api.user.get_users(
                groupname='bacon',
                group=bacon,
            )

    def test_get_users_nonexistent_group(self):
        """Test getting users for a group that does not exist."""

        from plone.api.exc import GroupNotFoundError
        with self.assertRaises(GroupNotFoundError):
            api.user.get_users(groupname='bacon')

    def test_delete_no_username(self):
        """Test deleting of a member with email login."""

        self._set_emaillogin(True)

        # This should fail either an username or user object should be given
        from plone.api.exc import MissingParameterError
        with self.assertRaises(MissingParameterError):
            api.user.delete()

        from plone.api.exc import InvalidParameterError
        with self.assertRaises(InvalidParameterError):
            api.user.delete(
                username='chuck@norris.org',
                user=mock.Mock(),
            )

        api.user.create(email='chuck@norris.org', password='secret')
        api.user.delete(username='unwanted@norris.org')

        user = api.user.create(email='steven@seagal.org', password='secret')
        api.user.delete(user=user)

    def test_delete_username(self):
        """test whether the user has been deleted."""

        api.user.create(
            username='unwanted',
            password='secret',
            email='unwanted@example.org',
        )
        api.user.delete(username='unwanted')

        user = api.user.create(
            username='steven',
            password='secret',
            email='steven@example.org',
        )
        api.user.delete(user=user)

    def test_is_anonymous(self):
        """Test anonymous access."""

        self.assertEqual(api.user.is_anonymous(), False)
        logout()
        self.assertEqual(api.user.is_anonymous(), True)

    def test_get_roles_username(self):
        """Test get roles passing a username."""
        ROLES = ['Reviewer', 'Editor']
        api.user.create(
            username='chuck',
            email='chuck@norris.org',
            password='secret',
            roles=ROLES,
        )
        if six.PY2:
            assertCountEqual = self.assertItemsEqual
        else:
            assertCountEqual = self.assertCountEqual
        assertCountEqual(
            ROLES + ['Authenticated'],
            api.user.get_roles(username='chuck'),
        )

    def test_get_roles_user(self):
        """Test get roles passing a user."""
        ROLES = ['Reviewer', 'Editor']
        user = api.user.create(
            username='chuck',
            email='chuck@norris.org',
            password='secret',
            roles=ROLES,
        )
        if six.PY2:
            assertCountEqual = self.assertItemsEqual
        else:
            assertCountEqual = self.assertCountEqual
        assertCountEqual(
            ROLES + ['Authenticated'],
            api.user.get_roles(user=user),
        )

    def test_get_roles_username_and_user(self):
        """Test get roles passing username and user."""
        ROLES = ['Reviewer', 'Editor']
        user = api.user.create(
            username='chuck',
            email='chuck@norris.org',
            password='secret',
            roles=ROLES,
        )

        from plone.api.exc import InvalidParameterError
        with self.assertRaises(InvalidParameterError):
            api.user.get_roles(
                username='chuck',
                user=user,
            )

    def test_get_roles_no_parameters(self):
        """Test get roles without any parameters."""
        if six.PY2:
            assertCountEqual = self.assertItemsEqual
        else:
            assertCountEqual = self.assertCountEqual
        assertCountEqual(
            ['Manager', 'Authenticated'],
            api.user.get_roles(),
        )

    def test_get_permissions_no_parameters(self):
        """Test get_permissions passing no parameters."""
        if six.PY2:
            assertCountEqual = self.assertItemsEqual
        else:
            assertCountEqual = self.assertCountEqual
        assertCountEqual(
            [p[0] for p in getPermissions()],
            api.user.get_permissions().keys(),
        )

    def test_get_roles_nonexistant_user(self):
        """Test get roles for a user that does not exist."""
        from plone.api.exc import UserNotFoundError
        with self.assertRaises(UserNotFoundError):
            api.user.get_roles(username='theurbanspaceman')

    def test_get_roles_anonymous(self):
        """Test get_roles for an anonymous user."""
        from AccessControl.users import nobody
        with api.env.adopt_user(user=nobody):
            self.assertEqual(
                api.user.get_roles(),
                ('Anonymous', ),
            )

    def test_get_roles_in_context(self):
        """Test get local and inherited roles for a user on an object"""
        api.user.create(
            username='chuck',
            email='chuck@norris.org',
            password='secret',
        )

        portal = api.portal.get()
        folder = api.content.create(
            container=portal,
            type='Folder',
            id='folder_one',
            title='Folder One',
        )
        document = api.content.create(
            container=folder,
            type='Document',
            id='document_one',
            title='Document One',
        )
        api.user.grant_roles(
            username='chuck',
            roles=['Editor'],
            obj=folder,
        )
        self.assertIn(
            'Editor',
            api.user.get_roles(username='chuck', obj=document),
        )

    def test_get_roles_local_only(self):
        """Test get local roles for a user on an object"""
        api.user.create(
            username='chuck',
            email='chuck@norris.org',
            password='secret',
        )

        portal = api.portal.get()
        folder = api.content.create(
            container=portal,
            type='Folder',
            id='folder_one',
            title='Folder One',
        )
        document = api.content.create(
            container=folder,
            type='Document',
            id='document_one',
            title='Document One',
        )
        api.user.grant_roles(
            username='chuck',
            roles=['Editor'],
            obj=folder,
        )
        self.assertNotIn(
            'Editor',
            api.user.get_roles(username='chuck', obj=document, inherit=False),
        )

    def test_get_roles_local_includes_group_roles(self):
        """Test if get local roles for a user on an object respects groups."""
        api.user.create(
            username='chuck',
            email='chuck@norris.org',
            password='secret',
        )
        api.group.create('foo', roles=['Reviewer'])
        api.group.add_user(groupname='foo', username='chuck')
        if six.PY2:
            assertCountEqual = self.assertItemsEqual
        else:
            assertCountEqual = self.assertCountEqual

        portal = api.portal.get()
        folder = api.content.create(
            container=portal,
            type='Folder',
            id='folder_one',
            title='Folder One',
        )
        document = api.content.create(
            container=folder,
            type='Document',
            id='document_one',
            title='Document One',
        )
        assertCountEqual(
            api.user.get_roles(username='chuck', obj=document),
            ['Member', 'Reviewer', 'Authenticated'],
        )
        api.user.grant_roles(
            username='chuck',
            roles=['Editor'],
            obj=folder,
        )
        assertCountEqual(
            api.user.get_roles(username='chuck', obj=document),
            ['Member', 'Reviewer', 'Authenticated', 'Editor'],
        )
        assertCountEqual(
            api.user.get_roles(username='chuck', obj=document, inherit=False),
            [],
        )
        assertCountEqual(
            api.user.get_roles(username='chuck', obj=folder, inherit=False),
            ['Editor'],
        )
        api.group.grant_roles(
            groupname='foo',
            roles=['Contributor'],
            obj=document,
        )
        assertCountEqual(
            ['Contributor'],
            api.user.get_roles(username='chuck', obj=document, inherit=False),
        )

    def test_get_permissions_root(self):
        """Test get permissions on site root."""

        user = api.user.create(
            username='chuck',
            email='chuck@norris.org',
            password='secret',
            roles=[],
        )

        from plone.api.exc import InvalidParameterError
        with self.assertRaises(InvalidParameterError):
            api.user.get_permissions(
                username='chuck',
                user=user,
            )

        PERMISSIONS = {
            'View': True,
            'Manage portal': False,
            'Modify portal content': False,
            'Access contents information': True,
        }

        for k, v in PERMISSIONS.items():
            self.assertEqual(
                v,
                api.user.get_permissions(username='chuck').get(k, None),
            )
            self.assertEqual(
                v,
                api.user.get_permissions(user=user).get(k, None),
            )

    def test_get_permissions_nonexistant_user(self):
        """Test get_permissions for a user that does not exist."""

        from plone.api.exc import UserNotFoundError
        with self.assertRaises(UserNotFoundError):
            api.user.get_permissions(username='ming')

    def test_get_permissions_context(self):
        """Test get permissions on some context."""

        user = api.user.create(
            username='chuck',
            email='chuck@norris.org',
            password='secret',
            roles=[],
        )

        from plone.api.exc import InvalidParameterError
        with self.assertRaises(InvalidParameterError):
            api.user.get_permissions(
                username='chuck',
                user=user,
            )

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
            title='Folder One',
        )

        for k, v in PERMISSIONS.items():
            self.assertEqual(
                v,
                api.user.get_permissions(
                    username='chuck',
                    obj=folder,
                ).get(k, None),
            )
            self.assertEqual(
                v,
                api.user.get_permissions(
                    user=user,
                    obj=folder,
                ).get(k, None),
            )

    def test_has_permission_context(self):
        """Test has_permission on some context."""

        username = 'billy'
        user = api.user.create(
            username=username,
            email='billy@bob.net',
            password='secret',
        )

        # Cannot supply both username and user arguments
        from plone.api.exc import InvalidParameterError
        with self.assertRaises(InvalidParameterError):
            api.user.has_permission(
                'View',
                username=username,
                user=user,
            )

        folder = api.content.create(
            container=self.portal,
            type='Folder',
            id='folder_one',
            title='A Folder',
        )
        api.content.transition(obj=folder, transition='publish')

        self.assertTrue(
            api.user.has_permission(
                'View',
                user=user,
                obj=folder,
            ),
        )
        self.assertFalse(
            api.user.has_permission(
                'Modify portal content',
                user=user,
                obj=folder,
            ),
        )

        self.assertTrue(
            api.user.has_permission(
                'View',
                user=None,
                obj=folder,
            ),
        )

    def test_grant_roles(self):
        """Test granting a couple of roles."""

        user = api.user.create(
            username='chuck',
            email='chuck@norris.org',
            password='secret',
        )

        api.user.grant_roles(username='chuck', roles=['Editor'])
        self.assertIn('Editor', api.user.get_roles(username='chuck'))
        self.assertIn('Editor', api.user.get_roles(user=user))

        api.user.grant_roles(username='chuck', roles=('Contributor',))
        self.assertIn('Contributor', api.user.get_roles(username='chuck'))
        self.assertIn('Contributor', api.user.get_roles(user=user))

        api.user.grant_roles(username='chuck', roles=['Reader', 'Reader'])
        ROLES = [
            'Editor',
            'Contributor',
            'Reader',
            'Authenticated',
            'Member',
        ]
        if six.PY2:
            assertCountEqual = self.assertItemsEqual
        else:
            assertCountEqual = self.assertCountEqual
        assertCountEqual(
            ROLES,
            api.user.get_roles(username='chuck'),
        )
        assertCountEqual(
            ROLES,
            api.user.get_roles(user=user),
        )

    def test_grant_roles_username_and_user(self):
        """Test grant roles passing username and user."""

        user = api.user.create(
            username='chuck',
            email='chuck@norris.org',
            password='secret',
        )

        from plone.api.exc import MissingParameterError
        with self.assertRaises(MissingParameterError):
            api.user.grant_roles(username=user)

        from plone.api.exc import InvalidParameterError
        with self.assertRaises(InvalidParameterError):
            api.user.grant_roles(username='chuck', roles=('Authenticated'))

    def test_grant_roles_anonymous(self):
        """Test granting Anonymous role."""

        from plone.api.exc import InvalidParameterError
        with self.assertRaises(InvalidParameterError):
            api.user.grant_roles(
                username='chuck',
                roles=['Anonymous'],
            )

    def test_grant_roles_authenticated(self):
        """Test granting Authenticated role."""
        from plone.api.exc import InvalidParameterError
        with self.assertRaises(InvalidParameterError):
            api.user.grant_roles(
                username='chuck',
                roles=['Authenticated'],
            )

    def test_grant_roles_no_parameters(self):
        """Test grant roles without passing parameters."""
        from plone.api.exc import MissingParameterError
        with self.assertRaises(MissingParameterError):
            api.user.grant_roles()

    def test_grant_roles_no_user(self):
        """If no user is found, raise a suitable error."""
        from plone.api.exc import InvalidParameterError
        with self.assertRaises(InvalidParameterError):
            api.user.grant_roles(
                username='chuck',
                roles=['Manager'],
            )

    def test_revoke_roles(self):
        """Test revoke roles."""

        user = api.user.create(
            username='chuck',
            email='chuck@norris.org',
            password='secret',
        )

        api.user.grant_roles(username='chuck', roles=['Reviewer', 'Editor'])
        api.user.revoke_roles(username='chuck', roles=['Reviewer'])
        self.assertNotIn('Reviewer', api.user.get_roles(username='chuck'))
        self.assertNotIn('Reviewer', api.user.get_roles(user=user))
        self.assertIn('Editor', api.user.get_roles(username='chuck'))
        self.assertIn('Editor', api.user.get_roles(user=user))

        api.user.revoke_roles(username='chuck', roles=('Editor',))
        ROLES = ['Authenticated', 'Member']
        if six.PY2:
            assertCountEqual = self.assertItemsEqual
        else:
            assertCountEqual = self.assertCountEqual

        assertCountEqual(
            ROLES,
            api.user.get_roles(username='chuck'),
        )
        assertCountEqual(
            ROLES,
            api.user.get_roles(user=user),
        )
        assertCountEqual(
            ROLES,
            api.user.get_roles(username='chuck', inherit=False),
        )
        assertCountEqual(
            ROLES,
            api.user.get_roles(user=user, inherit=False),
        )

    def test_revoke_roles_username_and_user(self):
        """Test revoke roles passing username and user."""

        user = api.user.create(
            username='chuck',
            email='chuck@norris.org',
            password='secret',
        )

        from plone.api.exc import MissingParameterError
        with self.assertRaises(MissingParameterError):
            api.user.revoke_roles(user=user)

    def test_revoke_roles_anonymous(self):
        """Test revoking Anonymous role."""

        from plone.api.exc import InvalidParameterError
        with self.assertRaises(InvalidParameterError):
            api.user.revoke_roles(
                username='chuck',
                roles=['Anonymous'],
            )

    def test_revoke_roles_authenticated(self):
        """Test revoking Authenticated role."""

        from plone.api.exc import InvalidParameterError
        with self.assertRaises(InvalidParameterError):
            api.user.revoke_roles(
                username='chuck',
                roles=['Authenticated'],
            )

    def test_revoke_roles_no_parameters(self):
        """Test revoke roles without passing parameters."""

        from plone.api.exc import MissingParameterError
        with self.assertRaises(MissingParameterError):
            api.user.revoke_roles()

    def test_revoke_roles_username(self):
        """Test revoke roles for username."""
        api.user.create(
            username='chuck',
            email='chuck@norris.org',
            password='secret',
        )
        from plone.api.exc import InvalidParameterError
        with self.assertRaises(InvalidParameterError):
            api.user.revoke_roles(username='chuck', roles=['Authenticated'])

    @unittest.skip('Getting the Anonymous user does not work like this.')
    def test_revoke_roles_from_anonymous(self):
        """Test revoking roles from an Anonymous user."""
        api.user.revoke_roles(
            username='Anonymous User',
            roles=['Reviewer'],
        )
        ROLES = ['Anonymous']
        self.assertCountEqual(
            ROLES,
            api.user.get_roles(username='Anonymous User'),
        )

    def test_revoke_roles_no_user(self):
        """If no user is found, raise a suitable error."""
        from plone.api.exc import InvalidParameterError
        with self.assertRaises(InvalidParameterError):
            api.user.revoke_roles(
                username='chuck',
                roles=['Manager'],
            )

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
            title='Folder One',
        )
        document = api.content.create(
            container=folder,
            type='Document',
            id='document_one',
            title='Document One',
        )

        api.user.grant_roles(
            username='chuck',
            roles=['Editor'],
            obj=folder,
        )
        self.assertIn(
            'Editor',
            api.user.get_roles(username='chuck', obj=folder),
        )
        if six.PY2:
            assertCountEqual = self.assertItemsEqual
        else:
            assertCountEqual = self.assertCountEqual
        assertCountEqual(
            ['Editor'],
            api.user.get_roles(username='chuck', obj=folder, inherit=False),
        )
        self.assertIn(
            'Editor',
            api.user.get_roles(user=user, obj=folder),
        )
        self.assertIn(
            'Editor',
            api.user.get_roles(username='chuck', obj=document),
        )
        self.assertIn(
            'Editor',
            api.user.get_roles(user=user, obj=document),
        )

        api.user.grant_roles(
            username='chuck',
            roles=('Contributor',),
            obj=folder,
        )
        self.assertIn(
            'Contributor',
            api.user.get_roles(username='chuck', obj=folder),
        )
        self.assertIn(
            'Contributor',
            api.user.get_roles(user=user, obj=folder),
        )
        self.assertIn(
            'Contributor',
            api.user.get_roles(username='chuck', obj=document),
        )
        self.assertIn(
            'Contributor',
            api.user.get_roles(user=user, obj=document),
        )

        ROLES = ['Editor', 'Contributor', 'Authenticated', 'Member']
        assertCountEqual(
            ROLES,
            api.user.get_roles(username='chuck', obj=folder),
        )
        assertCountEqual(
            ROLES,
            api.user.get_roles(user=user, obj=folder),
        )
        assertCountEqual(
            ROLES,
            api.user.get_roles(username='chuck', obj=document),
        )
        assertCountEqual(
            ROLES,
            api.user.get_roles(user=user, obj=document),
        )

    def test_grant_roles_disregards_adapter(self):
        """Test that borg.localrole-adpaters are not copied when granting
        local roles."""
        if six.PY2:
            assertCountEqual = self.assertItemsEqual
        else:
            assertCountEqual = self.assertCountEqual

        portal = api.portal.get()
        folder = api.content.create(
            container=portal,
            type='Folder',
            id='folder_one',
            title='Folder One',
        )
        document = api.content.create(
            container=folder,
            type='Document',
            id='document_one',
            title='Document One',
        )
        user = api.user.create(
            username='chuck',
            email='chuck@norris.org',
            password='secret',
        )

        assertCountEqual(
            api.user.get_roles(username='chuck', obj=folder),
            ['Member', 'Authenticated'],
        )
        self.assertFalse(
            api.user.get_roles(user=user, obj=folder, inherit=False),
        )

        # throw in a adapter granting the reviewer-roles
        @adapter(Interface)
        @implementer(ILocalRoleProvider)
        class LocalRoleProvider(object):

            def __init__(self, context):
                self.context = context

            def getRoles(self, principal_id):
                return ('Reviewer',)

        provideAdapter(LocalRoleProvider)

        # the adapter-role is added for get_role
        assertCountEqual(
            api.user.get_roles(username='chuck', obj=folder),
            ['Member', 'Authenticated', 'Reviewer'],
        )

        assertCountEqual(
            api.user.get_roles(username='chuck', obj=folder, inherit=False),
            ['Reviewer'],
        )

        # Assign a local role
        api.user.grant_roles(
            username='chuck',
            roles=['Contributor'],
            obj=folder,
        )
        assertCountEqual(
            api.user.get_roles(username='chuck', obj=folder),
            ['Member', 'Authenticated', 'Contributor', 'Reviewer'],
        )

        # The adapter role is in in the local roles but not persistent
        assertCountEqual(
            api.user.get_roles(username='chuck', obj=folder, inherit=False),
            ['Contributor', 'Reviewer'],
        )
        local_roles = getattr(folder, '__ac_local_roles__', {})
        self.assertEqual(
            local_roles.get('chuck'),
            ['Contributor'],
        )

        assertCountEqual(
            api.user.get_roles(username='chuck', obj=document, inherit=False),
            ['Reviewer'],
        )
        assertCountEqual(
            api.user.get_roles(username='chuck', obj=document),
            ['Member', 'Authenticated', 'Contributor', 'Reviewer'],
        )

        # add a group and test mix of group and adapter and user-roles
        api.group.create('foo')
        api.group.grant_roles(
            groupname='foo',
            roles=['Contributor'],
            obj=document,
        )
        api.group.add_user(groupname='foo', username='chuck')

        assertCountEqual(
            api.user.get_roles(username='chuck', obj=document, inherit=False),
            ['Contributor', 'Reviewer'],
        )
        api.group.grant_roles(groupname='foo', roles=['Manager'], obj=folder)
        assertCountEqual(
            api.user.get_roles(username='chuck', obj=document, inherit=False),
            ['Contributor', 'Reviewer'],
        )
        assertCountEqual(
            api.user.get_roles(username='chuck', obj=document),
            [
                'Contributor',
                'Reviewer',
                'Manager',
                'Authenticated',
                'Member',
            ],
        )
        assertCountEqual(
            api.user.get_roles(username='chuck', obj=folder),
            [
                'Contributor',
                'Reviewer',
                'Manager',
                'Authenticated',
                'Member',
            ],
        )
        assertCountEqual(
            api.user.get_roles(username='chuck', obj=folder, inherit=False),
            ['Contributor', 'Reviewer', 'Manager'],
        )

        # cleanup
        gsm = getGlobalSiteManager()
        gsm.unregisterAdapter(
            factory=LocalRoleProvider, provided=ILocalRoleProvider,
        )

    def test_revoke_roles_in_context(self):
        """Test revoke roles."""

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
            title='Folder One',
        )
        document = api.content.create(
            container=folder,
            type='Document',
            id='document_one',
            title='Document One',
        )
        api.user.grant_roles(
            username='chuck',
            roles=['Reviewer', 'Editor'],
            obj=folder,
        )

        api.user.revoke_roles(username='chuck', roles=['Reviewer'], obj=folder)
        self.assertIn(
            'Editor',
            api.user.get_roles(username='chuck', obj=folder),
        )
        self.assertIn('Editor', api.user.get_roles(user=user, obj=folder))
        self.assertIn(
            'Editor',
            api.user.get_roles(username='chuck', obj=document),
        )
        self.assertIn('Editor', api.user.get_roles(user=user, obj=document))
        self.assertNotIn(
            'Reviewer',
            api.user.get_roles(username='chuck', obj=folder),
        )
        self.assertNotIn('Reviewer', api.user.get_roles(user=user, obj=folder))
        self.assertNotIn(
            'Reviewer',
            api.user.get_roles(username='chuck', obj=document),
        )
        self.assertNotIn(
            'Reviewer',
            api.user.get_roles(user=user, obj=document),
        )

        api.user.revoke_roles(username='chuck', roles=['Editor'], obj=folder)
        self.assertNotIn(
            'Editor',
            api.user.get_roles(username='chuck', obj=folder),
        )
        self.assertNotIn('Editor', api.user.get_roles(user=user, obj=folder))
        self.assertNotIn(
            'Editor',
            api.user.get_roles(username='chuck', obj=document),
        )
        self.assertNotIn('Editor', api.user.get_roles(user=user, obj=document))

        ROLES = ['Authenticated', 'Member']
        if six.PY2:
            assertCountEqual = self.assertItemsEqual
        else:
            assertCountEqual = self.assertCountEqual
        assertCountEqual(
            ROLES,
            api.user.get_roles(username='chuck', obj=folder),
        )
        assertCountEqual(
            ROLES,
            api.user.get_roles(user=user, obj=folder),
        )
        assertCountEqual(
            ROLES,
            api.user.get_roles(username='chuck', obj=document),
        )
        assertCountEqual(
            ROLES,
            api.user.get_roles(user=user, obj=document),
        )
        assertCountEqual(
            [],
            api.user.get_roles(username='chuck', obj=folder, inherit=False),
        )
        assertCountEqual(
            [],
            api.user.get_roles(user=user, obj=folder, inherit=False),
        )
        assertCountEqual(
            [],
            api.user.get_roles(username='chuck', obj=document, inherit=False),
        )
        assertCountEqual(
            [],
            api.user.get_roles(user=user, obj=document, inherit=False),
        )
