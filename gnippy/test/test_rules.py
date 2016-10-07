# -*- coding: utf-8 -*-

try:
    import unittest2 as unittest
except ImportError:
    import unittest

import mock

from gnippy import rules
from gnippy.errors import *
from gnippy.test import test_utils


# Mocks
def bad_post(url, auth, data):
    return test_utils.BadResponse()


def good_post(url, auth, data):
    return test_utils.GoodResponse()


def bad_get(url, auth):
    return test_utils.BadResponse()


def get_exception(url, auth):
    raise Exception("This is a test exception")


def get_json_exception(url, auth):
    return test_utils.GoodResponseJsonError()


def good_get_no_rules_field(url, auth):
    return test_utils.GoodResponse(json={"hello": "world"})


def good_get_no_rules(url, auth):
    return test_utils.GoodResponse(json={"rules": []})


def good_get_one_rule(url, auth):
    return test_utils.GoodResponse(
        json={"rules": [{"value": "Hello", "tag": "mytag"}]})


def bad_delete(url, auth, data):
    return test_utils.BadResponse()


def good_delete(url, auth, data):
    return test_utils.GoodResponse()


class RulesTestCase(unittest.TestCase):
    rule_string = "Hello OR World"
    tag = "my_tag"

    def _generate_rules_list(self):
        rules_list = []
        rules_list.append(rules.build(self.rule_string))
        rules_list.append(rules.build(self.rule_string, self.tag))
        return rules_list

    def setUp(self):
        test_utils.generate_test_config_file()

    def tearDown(self):
        test_utils.delete_test_config()

    def test_build_post_object(self):
        """ Generate rules object to post. """
        rules_list = self._generate_rules_list()
        post_obj = rules._generate_post_object(rules_list)
        self.assertTrue("rules" in post_obj)
        rules._check_rules_list(post_obj['rules'])

    def test_check_one_rule_ok(self):
        """ Check list of one rule. """
        l = [{"value": "hello"}]
        rules._check_rules_list(l)

    def test_check_many_rules_ok(self):
        """ Check list of many rules. """
        l = [
            {"value": "hello", "id": 3},
            {"value": "goodbye", "tag": "w", "id": 4},
            {"value": "hi again", "tag": "x"},
            {"value": "bye again"}
        ]
        rules._check_rules_list(l)

    def test_check_rule_tag_none(self):
        """ Check list of rules both with tag and without. """
        l = [{"value": "hello", "tag": None}, {"value": "h", "tag": "w"}]
        rules._check_rules_list(l)

    def test_check_one_rule_typo_values(self):
        """ Make sure incorectly formatted rule values fail. """
        l = [{"values": "hello"}]
        try:
            rules._check_rules_list(l)
        except RulesListFormatException:
            return
        self.fail(
            "_check_rules_list was supposed to throw a RuleFormatException")

    def test_check_one_rule_typo_tag(self):
        """ Make sure incorrectly formatted rule tags fail. """
        l = [{"value": "hello", "tags": "t"}]
        try:
            rules._check_rules_list(l)
        except RulesListFormatException:
            return
        self.fail(
            "_check_rules_list was supposed to throw a RuleFormatException")

    def test_check_one_rule_extra_stuff_in_rule(self):
        """ Make sure rules with unexpected keys fail. """
        l = [{"value": "hello", "wat": "man"}]
        try:
            rules._check_rules_list(l)
        except RulesListFormatException:
            return
        self.fail(
            "_check_rules_list was supposed to throw a RuleFormatException")

    def test_build_rule_bad_args(self):
        """ Make sure building rules with unexpected args fail. """
        try:
            rules.build(None)
        except BadArgumentException:
            return
        self.fail(
            "rules.build_rule was supposed to throw a BadArgumentException")

    def test_build_rule_without_tag(self):
        """ Build rule without tag. """
        r = rules.build(self.rule_string)
        self.assertEqual(r['value'], self.rule_string)
        self.assertFalse("tag" in r)
        rules._check_rules_list([r])

    def test_build_rule_with_tag(self):
        """ Build rule with tag. """
        r = rules.build(self.rule_string, tag=self.tag)
        self.assertEqual(r['value'], self.rule_string)
        self.assertEqual(r['tag'], self.tag)
        rules._check_rules_list([r])

    @mock.patch('os.path.isfile', test_utils.os_file_exists_false)
    @mock.patch('requests.post', good_post)
    def test_add_one_rule_no_creds(self):
        """ Make sure adding rule without credentials fail. """
        try:
            rules.add_rule(self.rule_string, self.tag)
        except ConfigFileNotFoundException:
            return
        self.fail(
            "Rule Add was supposed to fail and throw a ConfigFileNotFoundException")

    @mock.patch('requests.post', good_post)
    def test_add_one_rule_ok(self):
        """Add one rule with config. """
        rules.add_rule(self.rule_string, self.tag,
                       config_file_path=test_utils.test_config_path)

    @mock.patch('requests.post', bad_post)
    def test_add_one_rule_not_ok(self):
        """Add one rule with exception thrown. """
        try:
            rules.add_rule(self.rule_string, self.tag,
                           config_file_path=test_utils.test_config_path)
        except RuleAddFailedException:
            return
        self.fail("Rule Add was supposed to fail and throw a RuleAddException")

    @mock.patch('os.path.isfile', test_utils.os_file_exists_false)
    @mock.patch('requests.post', good_post)
    def test_add_many_rules_no_creds(self):
        """ Make sure adding rules with non-existent config fails. """
        try:
            rules.add_rule(self.rule_string, self.tag)
        except ConfigFileNotFoundException:
            return
        self.fail(
            "Rule Add was supposed to fail and throw a ConfigFileNotFoundException")

    @mock.patch('requests.post', good_post)
    def test_add_many_rules_ok(self):
        """ Add many rules. """
        rules_list = self._generate_rules_list()
        rules.add_rules(rules_list,
                        config_file_path=test_utils.test_config_path)

    @mock.patch('requests.post', bad_post)
    def test_add_many_rules_not_ok(self):
        """ Add many rules with exception thrown. """
        try:
            rules_list = self._generate_rules_list()
            rules.add_rules(rules_list,
                            config_file_path=test_utils.test_config_path)
        except RuleAddFailedException:
            return
        self.fail("Rule Add was supposed to fail and throw a RuleAddException")

    @mock.patch('requests.get', get_exception)
    def test_get_rules_requests_get_exception(self):
        """ Get rules with exception thrown. """
        try:
            r = rules.get_rules(config_file_path=test_utils.test_config_path)
        except RulesGetFailedException:
            return
        self.fail("rules.get() was supposed to throw a RulesGetFailedException")

    @mock.patch('requests.get', bad_get)
    def test_get_rules_bad_status_code(self):
        """ Get rules with error response. """
        try:
            r = rules.get_rules(config_file_path=test_utils.test_config_path)
        except RulesGetFailedException as e:
            self.assertTrue("HTTP Status Code" in str(e))
            return
        self.fail("rules.get() was supposed to throw a RulesGetFailedException")

    @mock.patch('requests.get', get_json_exception)
    def test_get_rules_bad_json(self):
        """ Get rules with bad json response. """
        try:
            r = rules.get_rules(config_file_path=test_utils.test_config_path)
        except RulesGetFailedException as e:
            self.assertTrue("GNIP API returned malformed JSON" in str(e))
            return
        self.fail("rules.get() was supposed to throw a RulesGetFailedException")

    @mock.patch('requests.get', good_get_no_rules_field)
    def test_get_rules_no_rules_field_json(self):
        """ Get rules with invalid response. """
        try:
            r = rules.get_rules(config_file_path=test_utils.test_config_path)
        except RulesGetFailedException as e:
            self.assertTrue(
                "GNIP API response did not return a rules object" in str(e))
            return
        self.fail("rules.get() was supposed to throw a RulesGetFailedException")

    @mock.patch('requests.get', good_get_no_rules)
    def test_get_rules_success_no_rules(self):
        """ Get rules with empty response. """
        r = rules.get_rules(config_file_path=test_utils.test_config_path)
        self.assertEqual(0, len(r))

    @mock.patch('requests.get', good_get_one_rule)
    def test_get_rules_success_one_rule(self):
        """ Get one rule. """
        r = rules.get_rules(config_file_path=test_utils.test_config_path)
        self.assertEqual(1, len(r))

    @mock.patch('requests.post', good_delete)
    def test_delete_rules_single(self):
        """ Delete one rule. """
        rules.delete_rule({"value": "Hello World"},
                          config_file_path=test_utils.test_config_path)

    @mock.patch('requests.post', good_delete)
    def test_delete_rules_multiple(self):
        """ Delete multiple rules. """
        rules_list = [
            {"value": "Hello World"},
            {"value": "Hello", "tag": "mytag"}
        ]
        rules.delete_rules(rules_list,
                           config_file_path=test_utils.test_config_path)
