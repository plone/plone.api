# -*- coding: utf-8 -*-
"""Tests for plone.api.roles."""

from AccessControl import Unauthorized
from OFS.SimpleItem import SimpleItem
from plone import api
from plone.api.tests.base import INTEGRATION_TESTING
from plone.app.testing import TEST_USER_ID

import AccessControl
import unittest


class ExampleException(Exception):
    pass


role_mapping = (
    ('ppp', ('Manager', 'VIP', 'Member')),
    ('qqq', ('Manager', 'VIP')),
    ('rrr', ('Manager')),
)

# Version of Zope and Plone should be something like
# 'X.Y' or 'X.Y.Z' or 'X.Y.Z.A'
# It could also include a package status id (Alpha, Beta or RC).
# When run against coredev, we may have a .devN suffix as well.
version_regexp = r'^(\d+(\.\d+){1,3})(a\d+|b\d+|rc\d+)?(\.dev\d)?$'


class HasProtectedMethods(SimpleItem):

    security = AccessControl.ClassSecurityInfo()

    def __init__(self, id):
        self.id = id

    @security.public
    def public_method(self):
        pass

    @security.protected('ppp')
    def pp_method(self):
        pass

    @security.protected('qqq')
    def qq_method(self):
        pass

    @security.protected('rrr')
    def rr_method(self):
        pass

    @security.private
    def private_method(self):
        pass


AccessControl.class_init.InitializeClass(HasProtectedMethods)


class TestPloneApiEnv(unittest.TestCase):
    """Test plone.api.env"""

    layer = INTEGRATION_TESTING

    def setUp(self):
        """Shared test environment set-up, ran before every test."""
        portal = self.portal = self.layer['portal']
        portal._setObject('hpm', HasProtectedMethods('hpm'))

        # This isn't necessary to the unit tests, it makes debugging them
        # easier when they go wrong. Like "verbose-security on" in zope.conf
        sm = AccessControl.getSecurityManager()
        sm._policy._verbose = 1

        # Roles need to be created by name before we can assign permissions
        # to them or grant them to users.
        # 'Member' and 'Manager' already exist by default, we need to add 'VIP'
        portal._addRole('VIP')

        for permission, roles in role_mapping:
            portal.manage_permission(permission, roles, 1)

        api.user.create(
            username='worker',
            email='ordinary_person@example.com',
            password='password1',
            roles=('Member',),
        )

        api.user.create(
            username='boss',
            email='important_person@example.com',
            password='123456',
            roles=('Member', 'VIP'),
        )

        api.user.create(
            username='superhuman',
            email='xavier@example.com',
            password='think_carefully',
            roles=('Member', 'Manager'),
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
            with self.assertRaises(Unauthorized):
                self.portal.hpm.restrictedTraverse(name)

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

    def test_adopt_manager_string_role(self):
        """Test that we can adopt the Manager role temporarily."""
        with api.env.adopt_roles(roles='Manager'):
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

    def test_become_manager_by_name(self):
        """Tests that becoming a manager user works."""
        with api.env.adopt_user(username='superhuman'):
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

    def test_become_manager_by_obj(self):
        """Tests that becoming a manager with user from api.user works."""
        with api.env.adopt_user(user=api.user.get(username='superhuman')):
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

    def test_become_manager_by_acl_user(self):
        """Tests that becoming a user with user from acl_users works."""
        acl_users = api.portal.get().acl_users

        au_ordinary = acl_users.getUser('worker')
        with api.env.adopt_user(user=au_ordinary):
            self.should_allow([
                'public_method',
                'pp_method',
            ])
            self.should_forbid([
                'private_method',
                'qq_method',
                'rr_method',
            ])

        au_manager = acl_users.getUser('superhuman')
        with api.env.adopt_user(user=au_manager):
            self.should_allow([
                'public_method',
                'pp_method',
                'qq_method',
                'rr_method',
            ])
            self.should_forbid([
                'private_method',
            ])

    def test_become_ordinary(self):
        """Tests that becoming a user with fewer permissions works."""
        with api.env.adopt_user(username='worker'):
            self.should_allow([
                'public_method',
                'pp_method',
            ])
            self.should_forbid([
                'private_method',
                'qq_method',
                'rr_method',
            ])
        self.test_test_defaults()

    def test_adopted_content_ownership(self):
        """Tests that content created while user-switched is owned."""
        with api.env.adopt_user(username='superhuman'):
            doc3 = api.content.create(
                container=self.portal,
                type='Document',
                id='doc_3',
            )
        intended = self.portal.acl_users.getUser('superhuman')
        actual = doc3.getOwner()
        self.assertEqual(actual.getPhysicalPath(), intended.getPhysicalPath())

    def test_adopted_nested_ownership(self):
        """Test deep nesting of adopt_user and adopt_roles blocks."""
        with api.env.adopt_user(username='worker'):
            self.should_allow([
                'public_method',
                'pp_method',
            ])
            self.should_forbid([
                'private_method',
                'qq_method',
                'rr_method',
            ])
            with api.env.adopt_roles(['Anonymous']):
                self.should_allow([
                    'public_method',
                ])
                self.should_forbid([
                    'private_method',
                    'pp_method',
                    'qq_method',
                    'rr_method',
                ])
                with api.env.adopt_user(username='boss'):
                    self.should_allow([
                        'public_method',
                        'pp_method',
                        'qq_method',
                    ])
                    self.should_forbid([
                        'private_method',
                        'rr_method',
                    ])
                    with api.env.adopt_roles(['Manager']):
                        self.should_allow([
                            'public_method',
                            'pp_method',
                            'qq_method',
                            'rr_method',
                        ])
                        self.should_forbid([
                            'private_method',
                        ])

                        with api.env.adopt_roles(['Anonymous']):
                            self.should_allow([
                                'public_method',
                            ])
                            self.should_forbid([
                                'private_method',
                                'pp_method',
                                'qq_method',
                                'rr_method',
                            ])
                        # /roles Anonymous

                        doc4 = api.content.create(
                            container=self.portal,
                            type='Document',
                            id='doc_ock',
                        )
                        intended = self.portal.acl_users.getUser('boss')
                        intended_pp = intended.getPhysicalPath()
                        actual = doc4.getOwner()
                        actual_pp = actual.getPhysicalPath()
                        self.assertEqual(actual_pp, intended_pp)
                    # /roles Manager

                    self.should_allow([
                        'public_method',
                        'pp_method',
                        'qq_method',
                    ])
                    self.should_forbid([
                        'private_method',
                        'rr_method',
                    ])
                # /user boss

                self.should_allow([
                    'public_method',
                ])
                self.should_forbid([
                    'private_method',
                    'pp_method',
                    'qq_method',
                    'rr_method',
                ])
            # /roles Anonymous

            self.should_allow([
                'public_method',
                'pp_method',
            ])
            self.should_forbid([
                'private_method',
                'qq_method',
                'rr_method',
            ])
        # /user worker

    def test_adopting_zope_users(self):
        api.env.adopt_user(username='admin')
        api.env.adopt_user(user=api.user.get(username='admin'))

    def test_adopting_anonymous(self):
        from AccessControl.users import nobody
        self.assertNotEqual(nobody, api.user.get_current())
        with api.env.adopt_user(user=nobody):
            self.assertEqual(nobody, api.user.get_current())

    def test_empty_warning(self):
        """Tests that empty roles lists get warned about."""
        from plone.api.exc import InvalidParameterError
        with self.assertRaises(InvalidParameterError):
            api.env.adopt_roles([])

    def test_argument_requirement(self):
        """Tests that missing arguments don't go unnoticed."""
        from plone.api.exc import MissingParameterError
        with self.assertRaises(MissingParameterError):
            api.env.adopt_roles()

    def test_debug_mode(self):
        """Tests that the retured value is the same as
        getConfiguration.debug_mode."""
        from plone.api.env import debug_mode
        from App.config import getConfiguration
        getConfiguration().debug_mode = True
        self.assertEqual(debug_mode(), True)
        getConfiguration().debug_mode = False
        self.assertEqual(debug_mode(), False)

    def test_test_mode(self):
        """Tests that test_mode() returns True as we are in a test runner."""
        from plone.api.env import test_mode
        self.assertEqual(test_mode(), True)

    def test_read_only_mode(self):
        """Test that read_only_mode() returns False
        as we have a write enabled ZODB."""
        from plone.api.env import read_only_mode
        self.assertFalse(read_only_mode())

    def test_plone_version(self):
        """Tests that plone_version() returns Plone version."""
        from plone.api.env import plone_version
        self.assertTrue(isinstance(plone_version(), str))
        self.assertRegexpMatches(plone_version(), version_regexp)

    def test_zope_version(self):
        """Tests that zope_version() returns Zope version."""
        from plone.api.env import zope_version
        self.assertTrue(isinstance(zope_version(), str))
        self.assertRegexpMatches(zope_version(), version_regexp)

    def test_adopt_user_different_username(self):
        user = api.user.get(userid=TEST_USER_ID)
        with api.env.adopt_user(user=user):
            self.assertEqual(api.user.get_current().getId(), TEST_USER_ID)
