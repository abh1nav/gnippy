# -*- coding: utf-8 -*-

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


class RulesTestCase(unittest.TestCase):

    rule_string = "Hello OR World"
    tag = "my_tag"

    def _generate_rules_list(self):
        rules_list = []
        rules_list.append(rules.build_rule(self.rule_string))
        rules_list.append(rules.build_rule(self.rule_string, self.tag))
        return rules_list

    def setUp(self):
        test_utils.generate_test_config_file()

    def tearDown(self):
        test_utils.delete_test_config()

    def test_build_rules_url(self):
        url = "http://google.com/asdf.json"
        expected = "http://google.com/asdf/rules.json"
        rules_url = rules._generate_rules_url(url)
        self.assertEqual(expected, rules_url)

    def test_build_rules_url_bad(self):
        try:
            url = "http://google.com/asdf.xml"
            rules._generate_rules_url(url)
        except BadPowerTrackUrlException:
            return
        self.fail("_generate_rules_url was supposed to throw a BadPowerTrackUrlException")

    def test_build_post_object(self):
        rules_list = self._generate_rules_list()
        post_obj = rules._generate_post_object(rules_list)
        self.assertTrue("rules" in post_obj)
        rules._check_rules_list(post_obj['rules'])

    def test_check_one_rule_ok(self):
        l = [ { "value": "hello" } ]
        rules._check_rules_list(l)

    def test_check_many_rules_ok(self):
        l = [ { "value": "hello" }, { "value": "h", "tag": "w" }]
        rules._check_rules_list(l)

    def test_check_one_rule_typo_values(self):
        l = [ { "values": "hello" } ]
        try:
            rules._check_rules_list(l)
        except RulesListFormatException:
            return
        self.fail("_check_rules_list was supposed to throw a RuleFormatException")

    def test_check_one_rule_typo_tag(self):
        l = [ { "value": "hello", "tags": "t" } ]
        try:
            rules._check_rules_list(l)
        except RulesListFormatException:
            return
        self.fail("_check_rules_list was supposed to throw a RuleFormatException")

    def test_check_one_rule_extra_stuff_in_rule(self):
        l = [ { "value": "hello", "wat": "man" } ]
        try:
            rules._check_rules_list(l)
        except RulesListFormatException:
            return
        self.fail("_check_rules_list was supposed to throw a RuleFormatException")

    def test_build_rule_bad_args(self):
        try:
            rules.build_rule(None)
        except BadArgumentException:
            return
        self.fail("rules.build_rule was supposed to throw a BadArgumentException")

    def test_build_rule_without_tag(self):
        r = rules.build_rule(self.rule_string)
        self.assertEqual(r['value'], self.rule_string)
        self.assertFalse("tag" in r)
        rules._check_rules_list([r])

    def test_build_rule_with_tag(self):
        r = rules.build_rule(self.rule_string, tag=self.tag)
        self.assertEqual(r['value'], self.rule_string)
        self.assertEqual(r['tag'], self.tag)
        rules._check_rules_list([r])

    @mock.patch('os.path.isfile', test_utils.os_file_exists_false)
    @mock.patch('requests.post', good_post)
    def test_add_one_rule_no_creds(self):
        try:
            rules.add_rule(self.rule_string, self.tag)
        except ConfigFileNotFoundException:
            return
        self.fail("Rule Add was supposed to fail and throw a ConfigFileNotFoundException")

    @mock.patch('requests.post', good_post)
    def test_add_one_rule_ok(self):
        rules.add_rule(self.rule_string, self.tag, config_file_path=test_utils.test_config_path)

    @mock.patch('requests.post', bad_post)
    def test_add_one_rule_not_ok(self):
        try:
            rules.add_rule(self.rule_string, self.tag, config_file_path=test_utils.test_config_path)
        except RuleAddFailedException:
            return
        self.fail("Rule Add was supposed to fail and throw a RuleAddException")

    @mock.patch('os.path.isfile', test_utils.os_file_exists_false)
    @mock.patch('requests.post', good_post)
    def test_add_many_rules_no_creds(self):
        try:
            rules.add_rule(self.rule_string, self.tag)
        except ConfigFileNotFoundException:
            return
        self.fail("Rule Add was supposed to fail and throw a ConfigFileNotFoundException")

    @mock.patch('requests.post', good_post)
    def test_add_many_rules_ok(self):
        rules_list = self._generate_rules_list()
        rules.add_rules(rules_list, config_file_path=test_utils.test_config_path)

    @mock.patch('requests.post', bad_post)
    def test_add_many_rules_not_ok(self):
        try:
            rules_list = self._generate_rules_list()
            rules.add_rules(rules_list, config_file_path=test_utils.test_config_path)
        except RuleAddFailedException:
            return
        self.fail("Rule Add was supposed to fail and throw a RuleAddException")