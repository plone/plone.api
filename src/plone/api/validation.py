# -*- coding: utf-8 -*-
""" Decorators for validating parameters """

import inspect
from plone.api.exc import MissingParameterError


def _get_arg_spec(func, validator_args):
    """ Get the arguments specified in the function spec
    and check that the decorator doesn't refer to non-existant args """
    signature_args, _, _, _ = inspect.getargspec(func)

    extra_args = set(validator_args) - set(signature_args)
    if extra_args:
        raise ValueError(
            "Validator for %s refers to parameters that are \
not part of its signature: %s" % (
            func.__name__, ", ".join(extra_args),))

    return signature_args


def _get_supplied_args(signature_params, args, kwargs):
    """ make arg_name:value pairs for all args that have been passed in """
    supplied_args = {}
    for i in range(len(args)):
        supplied_args[signature_params[i]] = args[i]
    supplied_args.update(kwargs)
    return supplied_args


def required_parameters(*required_params):
    """ A decorator that tests whether all of the specified parameters
    have been supplied and are not None

    Todo: add an optional flag to allow None values through as valid parameters

    Usage:
    @required_parameters('a', 'b')
    def foo(a=None, b=None, c=None):
        pass
    """

    def _required_parameters(func):
        """ The actual decorator """

        signature_params = _get_arg_spec(func, required_params)

        def wrapped(*args, **kwargs):
            """ The wrapped function """

            supplied_args = _get_supplied_args(signature_params, args, kwargs)

            for p in required_params:
                if p not in supplied_args or supplied_args[p] is None:
                    raise MissingParameterError(
                        "Missing required parameter: %s" % p)

            return func(*args, **kwargs)

        return wrapped

    return _required_parameters
