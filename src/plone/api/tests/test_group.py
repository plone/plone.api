# -*- coding: utf-8 -*-
"""Tests for plone.api group."""
import mock
import unittest

from plone import api
from plone.api.tests.base import INTEGRATION_TESTING


class TestPloneApiContent(unittest.TestCase):
    """Unit tests for content manipulation using plone.api"""

    layer = INTEGRATION_TESTING

    def test_create(self):
        """ Test adding of a group """

        # Create a group for bacon lovers
        import pdb; pdb.set_trace()
        api.group.create('bacon-lovers')



    def test_get(self):
        """ Test adding of a group """

    def test_get_all(self):
        """ Test adding of a group """

    def test_delete(self):
        """ Test adding of a group """
