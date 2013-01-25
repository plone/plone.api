# -*- coding: utf-8 -*-
""" Decorators for validating parameters """

import inspect
from plone.api.exc import InvalidParameterError
from plone.api.exc import MissingParameterError


def required_parameters(required_params):
    """ This makes the decorator and passes it the list of
    required parameter names """

    if isinstance(required_params, basestring):
        required_params = (required_params,)

    def _required_parameters(func):
        """ The decorator """

        signature_params, _, _, _ = inspect.getargspec(func)
        if set(required_params) - set(signature_params):
            raise ValueError(
                "%s requires a parameter that is not part of its signature." \
                % func.__name__)

        def wrapped(*args, **kwargs):
            """ The wrapped function """
            assigned_params = set(signature_params[:len(args)] + kwargs.keys())

            for param in required_params:
                if param not in assigned_params:
                    raise MissingParameterError(
                        "Missing required parameter: %s" % param)

            return func(*args, **kwargs)

        return wrapped

    return _required_parameters
