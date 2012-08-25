class PloneApiError(Exception):
    """Base exception class for plone.api errors."""


class MissingParameterError(Exception):
    """Raised when a parameter is missing."""


class InvalidParameterError(Exception):
    """Raised when a parameter is invalid."""
