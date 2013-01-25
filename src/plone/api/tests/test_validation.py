# -*- coding: utf-8 -*-
"""Tests for plone.api.validation."""

from plone.api.tests.base import INTEGRATION_TESTING
from plone import api
from plone.api.validation import required_parameters
from plone.api.exc import InvalidParameterError
from plone.api.exc import MissingParameterError

import unittest2 as unittest


def undecorated_func(a=None, b=None, c=None):
    return 'bar'


class TestPloneAPIValidation(unittest.TestCase):
    """Test plone.api.validation."""

    layer = INTEGRATION_TESTING

    def test_single_keyword_arg_provided(self):
        """ Test for passing a single required parameter
        as a keyword argument """
        _func = required_parameters('a')(undecorated_func)
        self.assertEquals(_func(a='foo'), 'bar')

    def test_single_positional_arg_provided(self):
        """ Test for passing a single required parameter
        as a positional argument """
        _func = required_parameters('a')(undecorated_func)
        self.assertEquals(_func('foo'), 'bar')

    def test_single_arg_missing(self):
        """ Test that MissingParameterError is raised if the
        single required parameter is missing """
        _func = required_parameters('a')(undecorated_func)
        self.assertRaises(MissingParameterError, _func)

    def test_one_missing_one_provided(self):
        """ Test that MissingParameterError is raised if one of the
        required parameters is missing """
        _func = required_parameters(('a', 'b'))(undecorated_func)
        self.assertRaises(MissingParameterError, _func, 'foo')
