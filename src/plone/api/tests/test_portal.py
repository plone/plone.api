# -*- coding: utf-8 -*-
"""Tests for plone.api.portal."""
import unittest
from Products.CMFCore.utils import getToolByName

from plone.api import portal
from plone.api.tests.base import INTEGRATION_TESTING


class TestPloneApiPortal(unittest.TestCase):
    """Unit tests for getting portal info using plone.api"""

    layer = INTEGRATION_TESTING

    def setUp(self):
        """  """
        self.portal = self.layer['portal']

    def test_get(self):
        self.assertEqual(portal.get(), self.portal)

    def test_url(self):
        self.assertEqual(portal.url(), 'http://nohost/plone')

    def get_tool_constraints(self):
        """ Test the constraints for getting a tool. """

        # When no parameters are given an error is raised
        self.assertRaises(ValueError, portal.get_tool)

    def get_tool(self):
        self.assertEqual(portal.get_tool('portal_catalog'),
                         getToolByName(self.portal, 'portal_catalog'))
        self.assertEqual(portal.get_tool('portal_membership'),
                         getToolByName(self.portal, 'portal_membership'))
        self.assertEqual(portal.get_tool('non_existing'), None)
