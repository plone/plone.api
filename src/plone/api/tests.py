from unittest import TestCase
from plone.app.testing import PLONE_INTEGRATION_TESTING


class APITests(TestCase):

    layer = PLONE_INTEGRATION_TESTING

    def test_get_site(self):
        from plone.api import get_site
        site = get_site()
        self.assertEqual(site.getPortalTypeName(), 'Plone Site')
        self.assertEqual(site.getId(), 'plone')
