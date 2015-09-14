# -*- coding: utf-8 -*-
"""Tests for plone.api.validation."""

from plone.api.tests.base import INTEGRATION_TESTING
from plone.api.validation import _get_supplied_args as _gsa
from plone.api.validation import at_least_one_of
from plone.api.validation import mutually_exclusive_parameters
from plone.api.validation import required_parameters

import unittest


def undecorated_func(arg1=None, arg2=None, arg3=None):
    return 'foo'


class TestPloneAPIValidation(unittest.TestCase):
    """Test plone.api.validation."""

    layer = INTEGRATION_TESTING

    def test_decorator_works_the_same_as_explicit_calling(self):
        """Check that calling the decorator with the function as an argument
        is equivalent to decorating the function.
        """
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
        a parameter that doesn't exist in the function signature.
        """
        with self.assertRaises(ValueError):
            _func = required_parameters('arg1', 'wibble', 'wobble')
            _func(undecorated_func)

        with self.assertRaises(ValueError):
            _func = mutually_exclusive_parameters(
                'arg1',
                'wibble',
                'wobble'
            )
            _func(undecorated_func)

    def test_get_supplied_args(self):
        """Test that positional and keyword args are recognised correctly."""
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
        as a keyword argument.
        """
        _func = required_parameters('arg1')(undecorated_func)
        self.assertEquals(_func(arg1='hello'), 'foo')

    def test_single_positional_arg_provided(self):
        """Test for passing a single required parameter
        as a positional argument.
        """
        _func = required_parameters('arg1')(undecorated_func)
        self.assertEquals(_func('hello'), 'foo')

    def test_single_arg_missing(self):
        """Test that MissingParameterError is raised if the
        single required parameter is missing.
        """
        from plone.api.exc import MissingParameterError
        _func = required_parameters('arg1')(undecorated_func)
        with self.assertRaises(MissingParameterError):
            _func()

    def test_one_missing_one_provided(self):
        """Test that MissingParameterError is raised if only one of the
        required parameters is missing.
        """
        from plone.api.exc import MissingParameterError
        _func = required_parameters('arg1', 'arg2')(undecorated_func)
        with self.assertRaises(MissingParameterError):
            _func('hello')

    def test_no_mutually_exclusive_args_provided(self):
        """Test for passing no args (valid) to a function that specifies
        mutually exclusive parameters.
        """
        _func = mutually_exclusive_parameters('arg1', 'arg2')(undecorated_func)
        self.assertEquals(_func(), 'foo')
        self.assertEquals(_func(arg3='hello'), 'foo')

    def test_one_mutually_exclusive_arg_provided(self):
        """Test for passing one arg (the right number) to a function
        that specifies mutually exclusive parameters.
        """
        _func = mutually_exclusive_parameters('arg1', 'arg2')(undecorated_func)
        self.assertEquals(_func('hello'), 'foo')
        self.assertEquals(_func(arg1='hello'), 'foo')
        self.assertEquals(_func(arg2='hello'), 'foo')

    def test_two_mutually_exclusive_args_provided(self):
        """Test that InvalidParameterError is raised if more than
        one mutually exclusive argument is provided.
        """
        from plone.api.exc import InvalidParameterError
        _func = mutually_exclusive_parameters('arg1', 'arg2')(undecorated_func)
        with self.assertRaises(InvalidParameterError):
            _func('ahoy', 'there')

        with self.assertRaises(InvalidParameterError):
            _func(arg1='ahoy', arg2='there')

    def test_require_at_least_one_but_none_provided(self):
        """Test that MissingParameterError is raised if no argument is supplied
        when at least one is required.
        """
        from plone.api.exc import MissingParameterError
        _func = at_least_one_of('arg1', 'arg2')(undecorated_func)
        with self.assertRaises(MissingParameterError):
            _func()

    def test_require_at_least_one_and_one_provided(self):
        """Test for passing one argument when at least one is required."""
        _func = at_least_one_of('arg1', 'arg2')(undecorated_func)
        self.assertEquals(_func('ahoy'), 'foo')
        self.assertEquals(_func(arg2='ahoy'), 'foo')

    def test_require_at_least_one_and_several_provided(self):
        """Test for passing several arguments when at least one is required."""
        _func = at_least_one_of('arg1', 'arg2')(undecorated_func)
        self.assertEquals(_func('ahoy', 'there'), 'foo')
        self.assertEquals(_func(arg1='ahoy', arg2='there'), 'foo')
        self.assertEquals(_func('ahoy', arg2='there', arg3='matey'), 'foo')

    def test_required_and_mutually_exclusive(self):
        """Test that multiple decorators can be used together."""
        @mutually_exclusive_parameters('arg2', 'arg3')
        @required_parameters('arg1')
        def _func1_decorated(arg1=None, arg2=None, arg3=None):
            return 'foo'

        from plone.api.exc import InvalidParameterError
        from plone.api.exc import MissingParameterError

        # test that the required parameter error works (missing arg1)
        with self.assertRaises(MissingParameterError):
            _func1_decorated(arg2='ahoy')

        # test that the mutually exclusive decorator works
        # (arg2 and arg3 should not be there)
        with self.assertRaises(InvalidParameterError):
            _func1_decorated(
                arg1='ahoy',
                arg2='there',
                arg3='matey',
            )

        # test that they both work.  Making no assumptions here about the order
        # in which they fire.
        with self.assertRaises((InvalidParameterError, MissingParameterError)):
            _func1_decorated(
                arg2='ahoy',
                arg3='there',
            )

        # everything ok
        self.assertEqual(_func1_decorated('ahoy', arg3='there'), 'foo')

    def test_exactly_one_required(self):
        """Test that combining mutually_exclusive_parameters and
        at_least_one_of is equivalent to 'exactly one required'.
        """

        @mutually_exclusive_parameters('arg1', 'arg2')
        @at_least_one_of('arg1', 'arg2')
        def _func1_decorated(arg1=None, arg2=None, arg3=None):
            return 'foo'

        from plone.api.exc import InvalidParameterError
        from plone.api.exc import MissingParameterError

        # test it errors if you provide none
        with self.assertRaises(MissingParameterError):
            _func1_decorated()

        # test that it errors if you provide both
        with self.assertRaises(InvalidParameterError):
            _func1_decorated('ahoy', 'there')

        # everything ok
        self.assertEqual(_func1_decorated('ahoy'), 'foo')
        self.assertEqual(_func1_decorated('ahoy', arg3='there'), 'foo')
