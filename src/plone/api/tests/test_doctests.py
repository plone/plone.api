# -*- coding: utf-8 -*-
"""Boilerplate for doctest functional tests."""

import pkg_resources
from plone.app.testing import applyProfile
from plone.app.testing import setRoles
from plone.app.testing import PLONE_INTEGRATION_TESTING
from plone.app.testing import TEST_USER_ID
from plone.app.testing import TEST_USER_NAME
from plone.app.testing import TEST_USER_PASSWORD
from plone.testing import layered
from plone.testing.z2 import Browser
from zope.testing import renormalizing

import doctest
import manuel.codeblock
import manuel.doctest
import manuel.testing
import os
import re
import transaction
import unittest

try:
    pkg_resources.get_distribution('plone.app.contenttypes')
except pkg_resources.DistributionNotFound:
    HAS_PA_CONTENTTYPES = False
else:
    HAS_PA_CONTENTTYPES = True

FLAGS = (
    doctest.NORMALIZE_WHITESPACE |
    doctest.ELLIPSIS |
    doctest.REPORT_NDIFF |
    doctest.REPORT_ONLY_FIRST_FAILURE
)

CHECKER = renormalizing.RENormalizing([
    # Normalize the generated UUID values to always compare equal.
    (re.compile(
        r'[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}'),
        '<UUID>',
     ),
])


def setUp(self):  # pragma: no cover
    """Shared test environment set-up, ran before every test."""
    layer = self.globs['layer']
    # Update global variables within the tests.
    self.globs.update({
        'portal': layer['portal'],
        'request': layer['request'],
        'browser': Browser(layer['app']),
        'TEST_USER_NAME': TEST_USER_NAME,
        'TEST_USER_PASSWORD': TEST_USER_PASSWORD,
        'self': self,
    })

    portal = self.globs['portal']
    browser = self.globs['browser']

    browser.handleErrors = True
    portal.error_log._ignored_exceptions = ()

    setRoles(portal, TEST_USER_ID, ['Manager'])

    applyProfile(portal, 'Products.CMFPlone:plone')

    # Plone 5 support
    if HAS_PA_CONTENTTYPES:
        applyProfile(portal, 'plone.app.contenttypes:default')

    transaction.commit()


def DocFileSuite(
    testfile, flags=FLAGS, setUp=setUp, layer=PLONE_INTEGRATION_TESTING
):
    """Returns a test suite configured with a test layer.

    :param testfile: Path to a doctest file.
    :type testfile: str

    :param flags: Doctest test flags.
    :type flags: int

    :param setUp: Test set up function.
    :type setUp: callable

    :param layer: Test layer
    :type layer: object

    :rtype: `manuel.testing.TestSuite`
    """
    m = manuel.doctest.Manuel(optionflags=flags, checker=CHECKER)
    m += manuel.codeblock.Manuel()

    return layered(
        manuel.testing.TestSuite(
            m,
            testfile,
            setUp=setUp,
            globs=dict(layer=layer)
        ),
        layer=layer,
    )


def test_suite():
    """Find .rst files and test code examples in them."""
    path = 'doctests'
    doctests = []
    docs_path = os.path.join(os.path.dirname(__file__), path)

    for filename in os.listdir(docs_path):
        try:
            doctests.append(DocFileSuite(os.path.join(path, filename)))
        except IOError:
            print 'test_doctest.py skipping {0}'.format(filename)

    return unittest.TestSuite(doctests)
