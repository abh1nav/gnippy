# -*- coding: utf-8 -*-

import unittest

from gnippy import config as gnippy_config
from gnippy.test import test_utils
import os

class ConfigTestCase(unittest.TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        """ Delete the test config file at test_config_path """
        test_utils.delete_test_config()
        os.unsetenv("GNIPPY_URL")
        os.unsetenv("GNIPPY_AUTH_USERNAME")
        os.unsetenv("GNIPPY_AUTH_PASSWORD")

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

    def test_config_parsing_halt(self):
        """ Read the half config file and compare values. """
        test_utils.generate_test_config_file_with_only_auth()
        result = gnippy_config.get_config(test_utils.test_config_path)
        self.assertEqual(result['Credentials']['username'], test_utils.test_username)
        self.assertEqual(result['Credentials']['password'], test_utils.test_password)
        self.assertEqual(result['PowerTrack']['url'], None)

    def test_resolve_file_arg(self):
        """ Run the "resolve" method with just a filename and check if all info is loaded. """
        test_utils.generate_test_config_file()
        conf = gnippy_config.resolve({"config_file_path": test_utils.test_config_path})
        self.assertEqual(conf['auth'][0], test_utils.test_username)
        self.assertEqual(conf['auth'][1], test_utils.test_password)
        self.assertEqual(conf['url'], test_utils.test_powertrack_url)

    def test_resolve_conf_from_environment_variables(self):

        expected_url = test_utils.test_powertrack_url
        expected_username = test_utils.test_username
        expected_password = test_utils.test_password

        os.environ["GNIPPY_URL"] = expected_url
        os.environ["GNIPPY_AUTH_USERNAME"] = expected_username
        os.environ["GNIPPY_AUTH_PASSWORD"] = expected_password

        conf = gnippy_config.resolve({})
        self.assertEqual(conf['url'], test_utils.test_powertrack_url)
        self.assertEqual(conf['auth'][0], test_utils.test_username)
        self.assertEqual(conf['auth'][1], test_utils.test_password)
