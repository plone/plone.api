# -*- coding: utf-8 -*-
from plone.api.tests.base import INTEGRATION_TESTING
from plone import api
import unittest


class TestPloneSettings(unittest.TestCase):
    """Test that all plone.app.registry-based settings in CMFPlone can be
       looked up with get_registry_record.
    """
    layer = INTEGRATION_TESTING

    def setUp(self):
        self.portal = self.layer['portal']

    @unittest.skipIf(api.env.plone_version() <= '5.0b2', 'Plone 5 only')
    def test_editing_settings(self):
        keys = [
            'plone.available_editors',
            'plone.default_editor',
            'plone.ext_editor',
            'plone.enable_link_integrity_checks',
            'plone.lock_on_ttw_edit',
        ]
        for key in keys:
            raised = False
            try:
                api.portal.get_registry_record(key),
            except:
                raised = True
            self.assertFalse(raised, "'{}' not found in registry.".format(key))

    @unittest.skipIf(api.env.plone_version() <= '5.0b2', 'Plone 5 only')
    def test_language_settings(self):
        keys = [
            'plone.default_language',
            'plone.available_languages',
            'plone.use_combined_language_codes',
            'plone.display_flags',
            'plone.always_show_selector',
            'plone.use_content_negotiation',
            'plone.use_path_negotiation',
            'plone.use_cookie_negotiation',
            'plone.authenticated_users_only',
            'plone.set_cookie_always',
            'plone.use_subdomain_negotiation',
            'plone.use_cctld_negotiation',
            'plone.use_request_negotiation',
        ]
        for key in keys:
            raised = False
            try:
                api.portal.get_registry_record(key),
            except:
                raised = True
            self.assertFalse(raised, "'{}' not found in registry.".format(key))

    @unittest.skipIf(api.env.plone_version() <= '5.0b2', 'Plone 5 only')
    def test_filter_settings(self):
        keys = [
            'plone.disable_filtering',
            'plone.nasty_tags',
            'plone.stripped_tags',
            'plone.custom_tags',
            'plone.stripped_attributes',
            'plone.stripped_combinations',
            'plone.style_whitelist',
            'plone.class_blacklist',
        ]
        for key in keys:
            raised = False
            try:
                api.portal.get_registry_record(key),
            except:
                raised = True
            self.assertFalse(raised, "'{}' not found in registry.".format(key))

    @unittest.skipIf(api.env.plone_version() <= '5.0b2', 'Plone 5 only')
    def test_tinymce_settings(self):
        keys = [
            'plone.resizing',
            'plone.autoresize',
            'plone.editor_width',
            'plone.editor_height',
            'plone.content_css',
            'plone.header_styles',
            'plone.inline_styles',
            'plone.block_styles',
            'plone.alignment_styles',
            'plone.formats',
        ]
        for key in keys:
            raised = False
            try:
                api.portal.get_registry_record(key),
            except:
                raised = True
            self.assertFalse(raised, "'{}' not found in registry.".format(key))

    @unittest.skipIf(api.env.plone_version() <= '5.0b2', 'Plone 5 only')
    def test_tinymce_resource_types_settings(self):
        keys = [
            'plone.plugins',
            'plone.menubar',
            'plone.menu',
            'plone.templates',
            'plone.toolbar',
            'plone.custom_plugins',
            'plone.custom_buttons',
        ]
        for key in keys:
            raised = False
            try:
                api.portal.get_registry_record(key),
            except:
                raised = True
            self.assertFalse(raised, "'{}' not found in registry.".format(key))

    @unittest.skipIf(api.env.plone_version() <= '5.0b2', 'Plone 5 only')
    def test_tinymce_spellchecker_settings(self):
        keys = [
            'plone.libraries_spellchecker_choice',
            'plone.libraries_atd_ignore_strings',
            'plone.libraries_atd_show_types',
            'plone.libraries_atd_service_url',
        ]
        for key in keys:
            raised = False
            try:
                api.portal.get_registry_record(key),
            except:
                raised = True
            self.assertFalse(raised, "'{}' not found in registry.".format(key))

    @unittest.skipIf(api.env.plone_version() <= '5.0b2', 'Plone 5 only')
    def test_maintenance_settings(self):
        keys = [
            'plone.days',
        ]
        for key in keys:
            raised = False
            try:
                api.portal.get_registry_record(key),
            except:
                raised = True
            self.assertFalse(raised, "'{}' not found in registry.".format(key))

    @unittest.skipIf(api.env.plone_version() <= '5.0b2', 'Plone 5 only')
    def test_navigation_settings(self):
        keys = [
            'plone.generate_tabs',
            'plone.nonfolderish_tabs',
            'plone.displayed_types',
            'plone.filter_on_workflow',
            'plone.workflow_states_to_show',
            'plone.show_excluded_items',
        ]
        for key in keys:
            raised = False
            try:
                api.portal.get_registry_record(key),
            except:
                raised = True
            self.assertFalse(raised, "'{}' not found in registry.".format(key))

    @unittest.skipIf(api.env.plone_version() <= '5.0b2', 'Plone 5 only')
    def test_search_settings(self):
        keys = [
            'plone.enable_livesearch',
            'plone.types_not_searched',
            'plone.search_results_description_length',
        ]
        for key in keys:
            raised = False
            try:
                api.portal.get_registry_record(key),
            except:
                raised = True
            self.assertFalse(raised, "'{}' not found in registry.".format(key))

    @unittest.skipIf(api.env.plone_version() <= '5.0b2', 'Plone 5 only')
    def test_security_settings(self):
        keys = [
            'plone.enable_self_reg',
            'plone.enable_user_pwd_choice',
            'plone.enable_user_folders',
            'plone.allow_anon_views_about',
            'plone.use_email_as_login',
            'plone.use_uuid_as_userid',
        ]
        for key in keys:
            raised = False
            try:
                api.portal.get_registry_record(key),
            except:
                raised = True
            self.assertFalse(raised, "'{}' not found in registry.".format(key))

    @unittest.skipIf(api.env.plone_version() <= '5.0b2', 'Plone 5 only')
    def test_site_settings(self):
        keys = [
            'plone.site_title',
            'plone.site_logo',
            'plone.exposeDCMetaTags',
            'plone.enable_sitemap',
            'plone.webstats_js',
            'plone.display_publication_date_in_byline',
            'plone.icon_visibility',
            'plone.toolbar_position',
            'plone.toolbar_logo',
            'plone.robots_txt',
        ]
        for key in keys:
            raised = False
            try:
                api.portal.get_registry_record(key),
            except:
                raised = True
            self.assertFalse(raised, "'{}' not found in registry.".format(key))

    @unittest.skipIf(api.env.plone_version() <= '5.0b2', 'Plone 5 only')
    def test_date_and_time_settings(self):
        keys = [
            'plone.portal_timezone',
            'plone.available_timezones',
            'plone.first_weekday',
        ]
        for key in keys:
            raised = False
            try:
                api.portal.get_registry_record(key),
            except:
                raised = True
            self.assertFalse(raised, "'{}' not found in registry.".format(key))

    @unittest.skipIf(api.env.plone_version() <= '5.0b2', 'Plone 5 only')
    def test_mail_settings(self):
        keys = [
            'plone.smtp_host',
            'plone.smtp_port',
            'plone.smtp_userid',
            'plone.smtp_pass',
            'plone.email_from_name',
            'plone.email_from_address',
        ]
        for key in keys:
            raised = False
            try:
                api.portal.get_registry_record(key),
            except:
                raised = True
            self.assertFalse(raised, "'{}' not found in registry.".format(key))

    @unittest.skipIf(api.env.plone_version() <= '5.0b2', 'Plone 5 only')
    def test_markup_settings(self):
        keys = [
            'plone.default_type',
            'plone.allowed_types'
        ]
        for key in keys:
            raised = False
            try:
                api.portal.get_registry_record(key),
            except:
                raised = True
            self.assertFalse(raised, "'{}' not found in registry.".format(key))

    @unittest.skipIf(api.env.plone_version() <= '5.0b2', 'Plone 5 only')
    def test_users_and_groups_settings(self):
        keys = [
            'plone.many_groups',
            'plone.many_users'
        ]
        for key in keys:
            raised = False
            try:
                api.portal.get_registry_record(key),
            except:
                raised = True
            self.assertFalse(raised, "'{}' not found in registry.".format(key))

    @unittest.skipIf(api.env.plone_version() <= '5.0b2', 'Plone 5 only')
    def test_social_media_settings(self):
        keys = [
            'plone.share_social_data',
            'plone.twitter_username',
            'plone.facebook_app_id',
            'plone.facebook_username',
        ]
        for key in keys:
            raised = False
            try:
                api.portal.get_registry_record(key),
            except:
                raised = True
            self.assertFalse(raised, "'{}' not found in registry.".format(key))

    @unittest.skipIf(api.env.plone_version() <= '5.0b2', 'Plone 5 only')
    def test_imaging_settings(self):
        keys = [
            'plone.allowed_sizes',
            'plone.quality',
        ]
        for key in keys:
            raised = False
            try:
                api.portal.get_registry_record(key),
            except:
                raised = True
            self.assertFalse(raised, "'{}' not found in registry.".format(key))

    @unittest.skipIf(api.env.plone_version() <= '5.0b2', 'Plone 5 only')
    def test_login_settings(self):
        keys = [
            'plone.auth_cookie_length',
            'plone.verify_login_name',
            'plone.allow_external_login_sites',
            'plone.external_login_url',
            'plone.external_logout_url',
            'plone.external_login_iframe',
        ]
        for key in keys:
            raised = False
            try:
                api.portal.get_registry_record(key),
            except:
                raised = True
            self.assertFalse(raised, "'{}' not found in registry.".format(key))
