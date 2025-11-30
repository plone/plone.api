"""Shared internal typing aliases used across plone.api modules."""

from plone.dexterity.content import DexterityContent as DexterityContext
from Products.CMFCore.PortalFolder import PortalFolder
from typing import TypeAlias
from ZPublisher.HTTPRequest import HTTPRequest

# Public-facing context type for content APIs.
Content: TypeAlias = DexterityContext
Container: TypeAlias = PortalFolder

# Shared request type for browser/request-aware APIs.
Request: TypeAlias = HTTPRequest
