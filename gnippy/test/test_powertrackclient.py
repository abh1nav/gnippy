# -*- coding: utf-8 -*-

import os
from time import sleep

import mock

try:
    import unittest2 as unittest
except ImportError:
    import unittest

from gnippy import PowerTrackClient
from gnippy.test import test_utils


def _dummy_callback(activity):
    pass


class TestException(Exception):
    def __init__(self, message):
        self.message = message


def get_exception(*args, **kwargs):
    raise TestException("This is a test exception")


def iter_lines_generator():

    n = 0
    while True:

        yield "arbitrary string value {0}".format(n)
        n += 1

def get_request_stream(url, auth, stream):

    mocked_stream = mock.MagicMock()

    p = mock.PropertyMock()
    p.return_value = 200

    type(mocked_stream).status_code = p

    mocked_stream.iter_lines.side_effect = iter_lines_generator

    return mocked_stream


config_file = test_utils.test_config_path


class PowerTrackClientTestCase(unittest.TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        """ Remove the test config file. """
        test_utils.delete_test_config()

    def test_constructor_only_file(self):
        """ Initialize PowerTrackClient with only a config file path. """
        test_utils.generate_test_config_file()
        client = PowerTrackClient(_dummy_callback, config_file_path=config_file)
        expected_auth = (test_utils.test_username, test_utils.test_password)
        expected_url = test_utils.test_powertrack_url

        self.assertEqual(expected_auth[0], client.auth[0])
        self.assertEqual(expected_auth[1], client.auth[1])
        self.assertEqual(expected_url, client.url)

    def test_constructor_only_url(self):
        """
            Initialize PowerTrackClient with only urls.
            The config file is provided for testability.
        """
        test_utils.generate_test_config_file_with_only_auth()

        client = PowerTrackClient(_dummy_callback,
                                  url=test_utils.test_powertrack_url,
                                  config_file_path=config_file)
        expected_auth = (test_utils.test_username, test_utils.test_password)
        expected_url = test_utils.test_powertrack_url

        self.assertEqual(expected_auth[0], client.auth[0])
        self.assertEqual(expected_auth[1], client.auth[1])
        self.assertEqual(expected_url, client.url)

    def test_constructor_only_auth(self):
        """
            Initialize PowerTrackClient with only a config the auth tuple.
            The config file is provided for testability.
        """
        test_utils.generate_test_config_file_with_only_powertrack()

        expected_auth = (test_utils.test_username, test_utils.test_password)
        expected_url = test_utils.test_powertrack_url
        client = PowerTrackClient(_dummy_callback, auth=expected_auth, config_file_path=config_file)

        self.assertEqual(expected_auth[0], client.auth[0])
        self.assertEqual(expected_auth[1], client.auth[1])
        self.assertEqual(expected_url, client.url)

    def test_constructor_all_args(self):
        """ Initialize PowerTrackClient with all args. """
        test_utils.generate_test_config_file()
        expected_auth = ("hello", "world")
        expected_url = "http://wat.com/testing.json"
        client = PowerTrackClient(_dummy_callback, auth=expected_auth, url=expected_url, config_file_path=config_file)

        self.assertEqual(expected_auth[0], client.auth[0])
        self.assertEqual(expected_auth[1], client.auth[1])
        self.assertEqual(expected_url, client.url)

    def test_no_args(self):
        """ Check if a ~/.gnippy file is present and run a no-arg test. """
        possible_paths = test_utils.get_possible_config_locations()
        for config_path in possible_paths:
            if os.path.isfile(config_path):
                client = PowerTrackClient(_dummy_callback)
                self.assertIsNotNone(client.auth)
                self.assertIsNotNone(client.url)
                self.assertTrue("http" in client.url and "://" in client.url)

    @mock.patch('requests.get', get_exception)
    def test_exception_with_callback(self):
        """ When exception_callback is provided, worker uses it to communicate errors. """
        test_utils.generate_test_config_file()

        exception_callback = mock.Mock()

        client = PowerTrackClient(_dummy_callback, exception_callback,
                                  config_file_path=config_file)
        client.connect()
        client.disconnect()
        self.assertTrue(exception_callback.called)
        actual_exinfo = exception_callback.call_args[0][0]
        actual_ex = actual_exinfo[1]
        self.assertIsInstance(actual_ex, Exception)
        self.assertEqual(actual_ex.message, "This is a test exception")

    @mock.patch('requests.get', get_exception)
    def test_connected_status_after_exception_is_false(self):
        """ When an exception is thrown the client is no longer connected. """
        test_utils.generate_test_config_file()

        client = PowerTrackClient(_dummy_callback,
                                  config_file_path=config_file)
        client.connect()

        sleep(2)

        self.assertFalse(client.connected())

        client.disconnect()

    @mock.patch('requests.get', get_request_stream)
    def test_connected_status_true_when_running(self):
        """ Once the client connect method is called the client reports as connected. """
        test_utils.generate_test_config_file()

        client = PowerTrackClient(_dummy_callback,
                                  config_file_path=config_file)

        client.connect()

        self.assertTrue(client.connected())

        client.disconnect()

        self.assertFalse(client.connected())