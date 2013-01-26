# -*- coding: utf-8 -*-
"""Tests for plone.api.validation."""

from plone.api.exc import InvalidParameterError
from plone.api.exc import MissingParameterError
from plone.api.tests.base import INTEGRATION_TESTING
from plone.api.validation import mutually_exclusive_parameters
from plone.api.validation import required_parameters

import unittest2 as unittest


def undecorated_func(arg1=None, arg2=None, arg3=None):
    return 'foo'


class TestPloneAPIValidation(unittest.TestCase):
    """ Test plone.api.validation. """

    layer = INTEGRATION_TESTING

    def test_non_existant_required_arg(self):
        """ Test that ValueError is returned if the decorator requires
        a parameter that doesn't exist in the function signature """
        self.assertRaises(
            ValueError,
            required_parameters('arg1', 'wibble', 'wobble'),
            undecorated_func)

        self.assertRaises(
            ValueError,
            mutually_exclusive_parameters('arg1', 'wibble', 'wobble'),
            undecorated_func)

    def test_single_keyword_arg_provided(self):
        """ Test for passing a single required parameter
        as a keyword argument """
        _func = required_parameters('arg1')(undecorated_func)
        self.assertEquals(_func(arg1='hello'), 'foo')

    def test_single_positional_arg_provided(self):
        """ Test for passing a single required parameter
        as a positional argument """
        _func = required_parameters('arg1')(undecorated_func)
        self.assertEquals(_func('hello'), 'foo')

    def test_single_arg_missing(self):
        """ Test that MissingParameterError is raised if the
        single required parameter is missing """
        _func = required_parameters('arg1')(undecorated_func)
        self.assertRaises(MissingParameterError, _func)

    def test_single_arg_is_none(self):
        """ Test that MissingParameterError is raised if the
        single required parameter is None """
        _func = required_parameters('arg1')(undecorated_func)
        self.assertRaises(MissingParameterError, _func, None)

    def test_one_missing_one_provided(self):
        """ Test that MissingParameterError is raised if only one of the
        required parameters is missing """
        _func = required_parameters('arg1', 'arg2')(undecorated_func)
        self.assertRaises(MissingParameterError, _func, 'hello')

    def test_no_mutually_exclusive_args_provided(self):
        """ Test for passing no args (valid) to a function that specifies
        mutually exclusive parameters """
        _func = mutually_exclusive_parameters('arg1', 'arg2')(undecorated_func)
        self.assertEquals(_func(), 'foo')
        self.assertEquals(_func(arg3='hello'), 'foo')

    def test_one_mutually_exclusive_arg_provided(self):
        """ Test for passing one arg (the right number) to a function
        that specifies mutually exclusive parameters """
        _func = mutually_exclusive_parameters('arg1', 'arg2')(undecorated_func)
        self.assertEquals(_func('hello'), 'foo')
        self.assertEquals(_func(arg1='hello'), 'foo')
        self.assertEquals(_func(arg2='hello'), 'foo')

    def test_two_mutually_exclusive_args_provided(self):
        """ Test that InvalidParameterError is raised if more than
        one mutually exclusive argument is provided """
        _func = mutually_exclusive_parameters('arg1', 'arg2')(undecorated_func)
        self.assertRaises(InvalidParameterError, _func, 'ahoy', 'there')
        self.assertRaises(
            InvalidParameterError, _func, arg1='ahoy', arg2='there')
