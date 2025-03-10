"""Tests for plone.api.addon methods."""

from plone import api
from plone.api.addon import AddonInformation
from plone.api.tests.base import INTEGRATION_TESTING

import unittest


ADDON = "plone.session"


class TestAPIAddonGetAddons(unittest.TestCase):
    """TestCase for plone.api.addon.get_addons."""

    layer = INTEGRATION_TESTING

    def setUp(self):
        """Set up TestCase."""
        self.portal = self.layer["portal"]
        # Install plone.app.multilingual
        api.addon.install(ADDON)

    def test_api_get_addons(self):
        """Test api.addon.get_addons without any filter."""
        result = api.addon.get_addons()
        self.assertIsInstance(result, list)
        addon_ids = [addon.id for addon in result]
        self.assertIn(ADDON, addon_ids)

    def test_api_get_addons_limit_broken(self):
        """Test api.addon.get_addons filtering for broken add-ons."""
        result = api.addon.get_addons(limit="broken")
        self.assertEqual(len(result), 0)

    def test_api_get_addons_limit_non_installable(self):
        """Test api.addon.get_addons filtering for non_installable add-ons."""
        result = api.addon.get_addons(limit="non_installable")
        self.assertNotEqual(len(result), 0)
        addon_ids = [addon.id for addon in result]
        self.assertIn("plone.app.dexterity", addon_ids)

    def test_api_get_addons_limit_installed(self):
        """Test api.addon.get_addons filtering for installed add-ons."""
        result = api.addon.get_addons(limit="installed")
        self.assertEqual(len(result), 2)
        addon_ids = [addon.id for addon in result]
        self.assertIn(ADDON, addon_ids)

    def test_api_get_addons_limit_upgradable(self):
        """Test api.addon.get_addons filtering for add-ons with upgradable."""
        result = api.addon.get_addons(limit="upgradable")
        self.assertEqual(len(result), 0)

    def test_api_get_addons_limit_invalid(self):
        """Test api.addon.get_addons filtering with an invalid parameter."""
        with self.assertRaises(api.exc.InvalidParameterError) as cm:
            api.addon.get_addons(limit="foobar")
        self.assertIn("Parameter limit='foobar' is not valid.", str(cm.exception))

    def test_api_get_addon_ids(self):
        """Test api.addon.get_addon_ids."""
        result = api.addon.get_addon_ids(limit="installed")
        self.assertEqual(len(result), 2)
        self.assertIn(ADDON, result)


class TestAPIAddon(unittest.TestCase):
    """TestCase for plone.api.addon."""

    layer = INTEGRATION_TESTING

    def setUp(self):
        """Set up TestCase."""
        self.portal = self.layer["portal"]

    def test_api_install(self):
        """Test api.addon.install."""
        result = api.addon.install(ADDON)
        self.assertTrue(result)

    def test_api_uninstall(self):
        """Test api.addon.uninstall."""
        # First install the add-on
        api.addon.install(ADDON)
        # Then uninstall the add-on
        result = api.addon.uninstall(ADDON)
        self.assertTrue(result)

    def test_api_uninstall_unavailable(self):
        """Test api.addon.uninstall unavailable add-on."""
        result = api.addon.uninstall("Foobar")
        self.assertFalse(result)

    def test_api_get(self):
        """Test api.addon.get."""
        result = api.addon.get(ADDON)
        self.assertIsInstance(result, AddonInformation)
        self.assertEqual(result.id, ADDON)
        self.assertTrue(result.valid)
        self.assertEqual(result.description, "Optional plone.session refresh support.")
        self.assertEqual(result.profile_type, "default")
        self.assertIsInstance(result.version, str)
        self.assertIsInstance(result.install_profile, dict)
        self.assertIsInstance(result.uninstall_profile, dict)
        self.assertIsInstance(result.upgrade_info, dict)
