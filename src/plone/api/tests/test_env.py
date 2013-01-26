# -*- coding: utf-8 -*-
"""Tests for plone.api.roles."""

from AccessControl import Unauthorized
from OFS.SimpleItem import SimpleItem
from plone import api
from plone.api.tests.base import INTEGRATION_TESTING
import AccessControl
import AccessControl.SecurityManagement
import Globals
import unittest2 as unittest


role_mapping = (
    ('ppp', ('Manager', 'VIP', 'Member')),
    ('qqq', ('Manager', 'VIP')),
    ('rrr', ('Manager')),
)


class ExampleException(Exception):
    pass


class HasProtectedMethods(SimpleItem):

    security = AccessControl.ClassSecurityInfo()

    security.declarePublic('public_method')
    security.declareProtected('ppp', 'pp_method')
    security.declareProtected('qqq', 'qq_method')
    security.declareProtected('rrr', 'rr_method')
    security.declarePrivate('private_method')

    def __init__(self, id):
        self.id = id

    def public_method(self):
        pass

    def pp_method(self):
        pass

    def qq_method(self):
        pass

    def rr_method(self):
        pass

    def private_method(self):
        pass


Globals.InitializeClass(HasProtectedMethods)


class TestPloneApiRoles(unittest.TestCase):
    """Test plone.api.roles."""

    layer = INTEGRATION_TESTING

    def setUp(self):
        """Shared test environment set-up, ran before every test."""
        portal = self.portal = self.layer['portal']
        portal._setObject('hpm', HasProtectedMethods('hpm'))

        sm = AccessControl.getSecurityManager()
        sm._policy._verbose = 1

        for role in ('Member', 'VIP', 'Manager'):
            portal._addRole(role)

        for permission, roles in role_mapping:
            portal.manage_permission(permission, roles, 1)

        api.user.create(
            username='boss',
            email='important_person@example.com',
            password='123',
            roles=('Member', 'VIP')
        )

        self._old_sm = AccessControl.SecurityManagement.getSecurityManager()

        AccessControl.SecurityManagement.newSecurityManager(
            self.portal.REQUEST,
            self.portal.acl_users.getUser('boss'),
        )

    def tearDown(self):
        """Shared test environment clean-up, ran after every test."""
        AccessControl.SecurityManagement.setSecurityManager(self._old_sm)

    def should_allow(self, names):
        for name in names:
            self.portal.hpm.restrictedTraverse(name)

    def should_forbid(self, names):
        for name in names:
            self.assertRaises(
                Unauthorized,
                lambda: self.portal.hpm.restrictedTraverse(name)
            )

    def test_test_defaults(self):
        """Test that the default set-up does what I expect it to."""
        self.should_allow([
            'public_method',
            'pp_method',
            'qq_method',
        ])
        self.should_forbid([
            'rr_method',
            'private_method',
        ])

    def test_adopt_manager_role(self):
        """Test that we can adopt the Manager role temporarily."""
        with api.env.adopt_roles(roles=['Manager']):
            self.should_allow([
                'public_method',
                'pp_method',
                'qq_method',
                'rr_method',
            ])
            self.should_forbid([
                'private_method',
            ])
        self.test_test_defaults()

    def test_adopt_fewers_role(self):
        """Test that we can adopt a non-Manager role temporarily."""
        with api.env.adopt_roles(roles=['Member']):
            self.should_allow([
                'public_method',
                'pp_method',
            ])
            self.should_forbid([
                'qq_method',
                'rr_method',
                'private_method',
            ])
        self.test_test_defaults()

    def test_drop_to_anon(self):
        """Test that we can drop roles."""
        with api.env.adopt_roles(roles=['Anonymous']):
            self.should_allow([
                'public_method',
            ])
            self.should_forbid([
                'pp_method',
                'rr_method',
                'qq_method',
                'private_method',
            ])

    def test_content_owner_role(self):
        """Tests that adopting a role should not affect content ownership."""
        with api.env.adopt_roles(roles=['Manager']):
            doc2 = api.content.create(
                container=self.portal,
                type='Document',
                id='doc_2',
            )

        intended = self.portal.acl_users.getUser(api.user.get_current().id)
        actual = doc2.getOwner()
        self.assertEqual(actual.getPhysicalPath(), intended.getPhysicalPath())

    def test_empty_warning(self):
        """Tests that empty roles lists get warned about."""
        from plone.api.exc import InvalidParameterError
        self.assertRaises(
            InvalidParameterError,
            lambda: api.env.adopt_roles([])
        )

    def test_argument_requirement(self):
        """Tests that missing arguments don't go unnoticed."""
        from plone.api.exc import MissingParameterError
        self.assertRaises(
            MissingParameterError,
            lambda: api.env.adopt_roles()
        )
