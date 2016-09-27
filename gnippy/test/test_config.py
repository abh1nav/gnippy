# -*- coding: utf-8 -*-
try:
    import unittest2 as unittest
except ImportError:
    import unittest

from gnippy import config as gnippy_config
from gnippy.test import test_utils


class ConfigTestCase(unittest.TestCase):

    def setUp(self):
        test_utils.unset_environment_config_vars()

    def tearDown(self):
        """ Delete the test config file at test_config_path """
        test_utils.delete_test_config()
        test_utils.unset_environment_config_vars()

    def test_default_path(self):
        """
            Infer the user's home directory (either in /Users/.. or /home/..)
            and check if the default path produces the corrrect output.
        """
        possible_paths = test_utils.get_possible_config_locations()
        actual = gnippy_config.get_default_config_file_path()
        self.assertTrue(actual in possible_paths)

    def test_config_parsing_full(self):
        """ Read the test config and compare values. """
        test_utils.generate_test_config_file()
        result = gnippy_config.get_config(test_utils.test_config_path)
        self.assertEqual(result['Credentials']['username'], test_utils.test_username)
        self.assertEqual(result['Credentials']['password'], test_utils.test_password)
        self.assertEqual(result['PowerTrack']['url'], test_utils.test_powertrack_url)
        self.assertEqual(result['PowerTrack']['rules_url'], test_utils.test_rules_url)

    def test_config_parsing_halt(self):
        """ Read the half config file and compare values. """
        test_utils.generate_test_config_file_with_only_auth()
        result = gnippy_config.get_config(test_utils.test_config_path)
        self.assertEqual(result['Credentials']['username'], test_utils.test_username)
        self.assertEqual(result['Credentials']['password'], test_utils.test_password)
        self.assertEqual(result['PowerTrack']['url'], None)
        self.assertEqual(result['PowerTrack']['rules_url'], None)

    def test_resolve_file_arg(self):
        """ Run the "resolve" method with just a filename and check if all info is loaded. """
        test_utils.generate_test_config_file()
        conf = gnippy_config.resolve({"config_file_path": test_utils.test_config_path})
        self.assertEqual(conf['auth'][0], test_utils.test_username)
        self.assertEqual(conf['auth'][1], test_utils.test_password)
        self.assertEqual(conf['url'], test_utils.test_powertrack_url)
        self.assertEqual(conf['rules_url'], test_utils.test_rules_url)

    def test_resolve_conf_from_environment_variables(self):
        """ Run the "resolve" method providing env vars and check if all info is loaded. """
        test_utils.delete_test_config()
        test_utils.set_environment_config_vars()
        conf = gnippy_config.resolve({})
        self.assertEqual(conf['url'], test_utils.test_powertrack_url)
        self.assertEqual(conf['rules_url'], test_utils.test_rules_url)
        self.assertEqual(conf['auth'][0], test_utils.test_username)
        self.assertEqual(conf['auth'][1], test_utils.test_password)

    def test_resolve_conf_from_kwargs1(self):
        """ Run the "resolve" method providing kwargs and check if all info is loaded. """
        test_utils.delete_test_config()
        rules_url = 'http://gnip.rules.url'
        username = 'gnip-username'
        password = 'gnip-password'
        conf = gnippy_config.resolve({
            'rules_url': rules_url,
            'auth': (username, password)
        })
        self.assertEqual(conf['rules_url'], rules_url)
        self.assertEqual(conf['auth'][0], username)
        self.assertEqual(conf['auth'][1], password)

    def test_resolve_conf_from_kwargs2(self):
        """ Run the "resolve" method providing kwargs and check if all info is loaded. """
        test_utils.delete_test_config()
        url = 'http://gnip.url'
        username = 'gnip-username'
        password = 'gnip-password'
        conf = gnippy_config.resolve({
            'url': url,
            'auth': (username, password)
        })
        self.assertEqual(conf['url'], url)
        self.assertEqual(conf['auth'][0], username)
        self.assertEqual(conf['auth'][1], password)
