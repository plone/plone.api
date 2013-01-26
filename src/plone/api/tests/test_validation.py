# -*- coding: utf-8 -*-
"""Tests for plone.api.validation."""

from plone.api.exc import InvalidParameterError
from plone.api.exc import MissingParameterError
from plone.api.tests.base import INTEGRATION_TESTING
from plone.api.validation import _get_supplied_args as _gsa
from plone.api.validation import mutually_exclusive_parameters
from plone.api.validation import required_parameters

import unittest2 as unittest


def undecorated_func(arg1=None, arg2=None, arg3=None):
    return 'foo'


class TestPloneAPIValidation(unittest.TestCase):
    """Test plone.api.validation."""

    layer = INTEGRATION_TESTING

    def test_decorator_works_the_same_as_explicit_calling(self):
        """Check that calling the decorator with the function as an argument
        is equivalent to decorating the function"""
        @required_parameters('arg1')
        def _func1_decorated(arg1=None, arg2=None, arg3=None):
            """This is my docstring"""
            pass

        def _func2_undecorated(arg1=None, arg2=None, arg3=None):
            """This is my docstring"""
            pass
        _func2_decorated = required_parameters('arg1')(_func2_undecorated)

        # Check that the decorated function gets the correct docstring
        self.assertEquals(_func1_decorated.__doc__, 'This is my docstring')

        # Check that both functions have the same docstring
        self.assertEquals(_func1_decorated.__doc__, _func2_decorated.__doc__)

    def test_non_existant_required_arg(self):
        """Test that ValueError is returned if the decorator requires
        a parameter that doesn't exist in the function signature
        """
        self.assertRaises(
            ValueError,
            required_parameters('arg1', 'wibble', 'wobble'),
            undecorated_func)

        self.assertRaises(
            ValueError,
            mutually_exclusive_parameters('arg1', 'wibble', 'wobble'),
            undecorated_func)

    def test_get_supplied_args(self):
        """Test that positional and keyword args are recognised correctly"""
        # the arguments specified in the function signature
        signature = ('arg1', 'arg2', 'arg3')

        # test that positional args are recognised correctly
        result = _gsa(signature, ('foo', 'wibble'), {})
        self.assertEquals(set(result), set(('arg1', 'arg2')))

        # test that keyword args are recognised correctly
        result = _gsa(
            signature, (), {'arg1': 'foo', 'arg2': 'wibble'})
        self.assertEquals(set(result), set(('arg1', 'arg2')))

        # test that a mixture of args are recognised correctly
        result = _gsa(signature, ('foo',), {'arg2': 'wibble'})
        self.assertEquals(set(result), set(('arg1', 'arg2')))

        # test that None-valued positional args are ignored
        result = _gsa(
            signature, ('foo', None), {})
        self.assertEquals(set(result), set(('arg1',)))

        # test that None-valued keyword args are ignored
        result = _gsa(
            signature, (), {'arg1': None, 'arg2': 'wibble'})
        self.assertEquals(set(result), set(('arg2',)))

    def test_single_keyword_arg_provided(self):
        """Test for passing a single required parameter
        as a keyword argument
        """
        _func = required_parameters('arg1')(undecorated_func)
        self.assertEquals(_func(arg1='hello'), 'foo')

    def test_single_positional_arg_provided(self):
        """Test for passing a single required parameter
        as a positional argument
        """
        _func = required_parameters('arg1')(undecorated_func)
        self.assertEquals(_func('hello'), 'foo')

    def test_single_arg_missing(self):
        """Test that MissingParameterError is raised if the
        single required parameter is missing
        """
        _func = required_parameters('arg1')(undecorated_func)
        self.assertRaises(MissingParameterError, _func)

    def test_one_missing_one_provided(self):
        """Test that MissingParameterError is raised if only one of the
        required parameters is missing
        """
        _func = required_parameters('arg1', 'arg2')(undecorated_func)
        self.assertRaises(MissingParameterError, _func, 'hello')

    def test_no_mutually_exclusive_args_provided(self):
        """Test for passing no args (valid) to a function that specifies
        mutually exclusive parameters
        """
        _func = mutually_exclusive_parameters('arg1', 'arg2')(undecorated_func)
        self.assertEquals(_func(), 'foo')
        self.assertEquals(_func(arg3='hello'), 'foo')

    def test_one_mutually_exclusive_arg_provided(self):
        """Test for passing one arg (the right number) to a function
        that specifies mutually exclusive parameters
        """
        _func = mutually_exclusive_parameters('arg1', 'arg2')(undecorated_func)
        self.assertEquals(_func('hello'), 'foo')
        self.assertEquals(_func(arg1='hello'), 'foo')
        self.assertEquals(_func(arg2='hello'), 'foo')

    def test_two_mutually_exclusive_args_provided(self):
        """Test that InvalidParameterError is raised if more than
        one mutually exclusive argument is provided
        """
        _func = mutually_exclusive_parameters('arg1', 'arg2')(undecorated_func)
        self.assertRaises(InvalidParameterError, _func, 'ahoy', 'there')
        self.assertRaises(
            InvalidParameterError, _func, arg1='ahoy', arg2='there')
