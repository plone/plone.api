# -*- coding: utf-8 -*-
"""Base module for unittesting."""

import unittest2 as unittest

from plone.app.testing import FunctionalTesting
from plone.app.testing import IntegrationTesting
from plone.app.testing import PLONE_FIXTURE
from plone.app.testing import PloneSandboxLayer
from plone.app.testing import TEST_USER_NAME
from plone.app.testing import TEST_USER_ID
from plone.app.testing import login
from plone.app.testing import setRoles
from plone.app.testing import applyProfile
from plone.testing import z2


class PloneApiLayer(PloneSandboxLayer):

    defaultBases = (PLONE_FIXTURE,)

    def setUpZope(self, app, configurationContext):
        """Set up Zope."""
        # Load ZCML
#        import plone.api
#        self.loadZCML(package=plone.api)
#        z2.installProduct(app, 'plone.api')

    def setUpPloneSite(self, portal):
        """Set up Plone."""
        # Install into Plone site using portal_setup
#        applyProfile(portal, 'plone.api:default')

        # Login as manager
        setRoles(portal, TEST_USER_ID, ['Manager'])
        login(portal, TEST_USER_NAME)


    def tearDownZope(self, app):
        """Tear down Zope."""
        z2.uninstallProduct(app, 'plone.api')


FIXTURE = PloneApiLayer()
INTEGRATION_TESTING = IntegrationTesting(
    bases=(FIXTURE,), name="PloneApiLayer:Integration")
FUNCTIONAL_TESTING = FunctionalTesting(
    bases=(FIXTURE,), name="PloneApiLayer:Functional")
