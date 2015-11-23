#!env/bin/python
"""Test cases for pymailcheck.

Adapted from https://github.com/mailcheck/mailcheck/blob/master/spec/\
mailcheckSpec.js.
"""

import unittest
import pymailcheck

DOMAINS = (
    "google.com",
    "gmail.com",
    "emaildomain.com",
    "comcast.net",
    "facebook.com",
    "msn.com",
    "gmx.de",
)

SECOND_LEVEL_DOMAINS = (
    "yahoo",
    "hotmail",
    "mail",
    "live",
    "outlook",
    "gmx",
)

TOP_LEVEL_DOMAINS = (
    "co.uk",
    "com",
    "org",
    "info",
    "fr",
)


class Sift3DistanceTestCase(unittest.TestCase):
    def test_sift3_distance(self):
        self.assertEqual(pymailcheck.sift3_distance("boat", "boot"), 1)
        self.assertEqual(pymailcheck.sift3_distance("boat", "bat"), 1.5)
        self.assertEqual(pymailcheck.sift3_distance("ifno", "info"), 2)
        self.assertEqual(pymailcheck.sift3_distance("hotmial", "hotmail"), 2)


class SplitEmailTestCase(unittest.TestCase):
    def test_one_level_domain(self):
        parts = pymailcheck.split_email("postbox@com")
        expected = {
            "address": "postbox",
            "domain": "com",
            "top_level_domain": "com",
            "second_level_domain": "",
        }
        self.assertEqual(parts, expected)

    def test_two_level_domain(self):
        parts = pymailcheck.split_email("test@example.com")
        expected = {
            "address": "test",
            "domain": "example.com",
            "top_level_domain": "com",
            "second_level_domain": "example",
        }
        self.assertEqual(parts, expected)

    def test_three_level_domain(self):
        parts = pymailcheck.split_email("test@example.co.uk")
        expected = {
            "address": "test",
            "domain": "example.co.uk",
            "top_level_domain": "co.uk",
            "second_level_domain": "example",
        }
        self.assertEqual(parts, expected)

    def test_four_level_domain(self):
        parts = pymailcheck.split_email("test@mail.randomsmallcompany.co.uk")
        expected = {
            "address": "test",
            "domain": "mail.randomsmallcompany.co.uk",
            "top_level_domain": "randomsmallcompany.co.uk",
            "second_level_domain": "mail",
        }
        self.assertEqual(parts, expected)

    def test_rfc_compliant(self):
        parts = pymailcheck.split_email('"foo@bar"@example.com')
        expected = {
            "address": '"foo@bar"',
            "domain": "example.com",
            "top_level_domain": "com",
            "second_level_domain": "example",
        }
        self.assertEqual(parts, expected)

    def test_contains_numbers(self):
        parts = pymailcheck.split_email("containsnumbers1234567890@example.com")
        expected = {
            "address": "containsnumbers1234567890",
            "domain": "example.com",
            "top_level_domain": "com",
            "second_level_domain": "example",
        }
        self.assertEqual(parts, expected)

    def test_contains_plus(self):
        parts = pymailcheck.split_email("contains+symbol@example.com")
        expected = {
            "address": "contains+symbol",
            "domain": "example.com",
            "top_level_domain": "com",
            "second_level_domain": "example",
        }
        self.assertEqual(parts, expected)

    def test_contains_hyphen(self):
        parts = pymailcheck.split_email("contains-symbol@example.com")
        expected = {
            "address": "contains-symbol",
            "domain": "example.com",
            "top_level_domain": "com",
            "second_level_domain": "example",
        }
        self.assertEqual(parts, expected)

    def test_contains_periods(self):
        parts = pymailcheck.split_email("contains.symbol@domain.contains.symbol")
        expected = {
            "address": "contains.symbol",
            "domain": "domain.contains.symbol",
            "top_level_domain": "contains.symbol",
            "second_level_domain": "domain",
        }
        self.assertEqual(parts, expected)

    def test_contains_period_backslash(self):
        parts = pymailcheck.split_email('"contains.and\ symbols"@example.com')
        expected = {
            "address": '"contains.and\ symbols"',
            "domain": "example.com",
            "top_level_domain": "com",
            "second_level_domain": "example",
        }
        self.assertEqual(parts, expected)

    def test_contains_period_at_sign(self):
        parts = pymailcheck.split_email('"contains.and.@.symbols.com"@example.com')
        expected = {
            "address": '"contains.and.@.symbols.com"',
            "domain": "example.com",
            "top_level_domain": "com",
            "second_level_domain": "example",
        }
        self.assertEqual(parts, expected)

    def test_contains_all_symbols(self):
        parts = pymailcheck.split_email('"()<>[]:;@,\\\"!#$%&\'*+-/=?^_`{}|\ \ \ \ \ ~\ \ \ \ \ \ \ ?\ \ \ \ \ \ \ \ \ \ \ \ ^_`{}|~.a"@allthesymbols.com')
        expected = {
            "address": '"()<>[]:;@,\\\"!#$%&\'*+-/=?^_`{}|\ \ \ \ \ ~\ \ \ \ \ \ \ ?\ \ \ \ \ \ \ \ \ \ \ \ ^_`{}|~.a"',
            "domain": "allthesymbols.com",
            "top_level_domain": "com",
            "second_level_domain": "allthesymbols",
        }
        self.assertEqual(parts, expected)

    def test_not_rfc_compliant(self):
        self.assertFalse(pymailcheck.split_email("example.com"))
        self.assertFalse(pymailcheck.split_email("abc.example.com"))
        self.assertFalse(pymailcheck.split_email("@example.com"))
        self.assertFalse(pymailcheck.split_email("test@"))

    def test_trim_spaces(self):
        parts = pymailcheck.split_email(" postbox@com")
        expected = {
            "address": "postbox",
            "domain": "com",
            "top_level_domain": "com",
            "second_level_domain": "",
        }
        self.assertEqual(parts, expected)
        parts = pymailcheck.split_email("postbox@com ")
        self.assertEqual(parts, expected)

    def test_most_similar_domain(self):
        self.assertEqual(
            pymailcheck.find_closest_domain("google.com", DOMAINS),
            "google.com"
        )
        self.assertEqual(
            pymailcheck.find_closest_domain("gmail.com", DOMAINS),
            "gmail.com"
        )
        self.assertEqual(
            pymailcheck.find_closest_domain("emaildomain.com", DOMAINS),
            "emaildomain.com"
        )
        self.assertEqual(
            pymailcheck.find_closest_domain("gmsn.com", DOMAINS),
            "msn.com"
        )
        self.assertEqual(
            pymailcheck.find_closest_domain("gmaik.com", DOMAINS),
            "gmail.com"
        )

    def test_most_similar_second_level_domain(self):
        self.assertEqual(
            pymailcheck.find_closest_domain("hotmial", SECOND_LEVEL_DOMAINS),
            "hotmail"
        )
        self.assertEqual(
            pymailcheck.find_closest_domain("tahoo", SECOND_LEVEL_DOMAINS),
            "yahoo"
        )
        self.assertEqual(
            pymailcheck.find_closest_domain("livr", SECOND_LEVEL_DOMAINS),
            "live"
        )
        self.assertEqual(
            pymailcheck.find_closest_domain("outllok", SECOND_LEVEL_DOMAINS),
            "outlook"
        )

    def test_most_similar_top_level_domain(self):
        self.assertEqual(
            pymailcheck.find_closest_domain("cmo", TOP_LEVEL_DOMAINS),
            "com"
        )
        self.assertEqual(
            pymailcheck.find_closest_domain("ogr", TOP_LEVEL_DOMAINS),
            "org"
        )
        self.assertEqual(
            pymailcheck.find_closest_domain("ifno", TOP_LEVEL_DOMAINS),
            "info"
        )
        self.assertEqual(
            pymailcheck.find_closest_domain("com.uk", TOP_LEVEL_DOMAINS),
            "co.uk"
        )


class SuggestTestCast(unittest.TestCase):
    def test_returns_array(self):
        expected = {
            "address": "test",
            "domain": "gmail.com",
            "full": "test@gmail.com",
        }
        self.assertEqual(
            pymailcheck.suggest("test@gmail.co", DOMAINS),
            expected
        )

    def test_no_suggestion_returns_false(self):
        self.assertFalse(
            pymailcheck.suggest("contact@kicksend.com", DOMAINS),
        )

    def test_incomplete_email_returns_false(self):
        self.assertFalse(
            pymailcheck.suggest("", DOMAINS),
        )
        self.assertFalse(
            pymailcheck.suggest("test@", DOMAINS),
        )
        self.assertFalse(
            pymailcheck.suggest("test", DOMAINS),
        )

    def test_returns_valid_suggestions(self):
        self.assertEqual(
            pymailcheck.suggest("test@gmailc.om", DOMAINS)["domain"],
            "gmail.com"
        )
        self.assertEqual(
            pymailcheck.suggest("test@emaildomain.co", DOMAINS)["domain"],
            "emaildomain.com"
        )
        self.assertEqual(
            pymailcheck.suggest("test@gmail.con", DOMAINS)["domain"],
            "gmail.com"
        )
        self.assertEqual(
            pymailcheck.suggest("test@gnail.con", DOMAINS)["domain"],
            "gmail.com"
        )
        self.assertEqual(
            pymailcheck.suggest("test@GNAIL.con", DOMAINS)["domain"],
            "gmail.com"
        )
        self.assertEqual(
            pymailcheck.suggest("test@#gmail.com", DOMAINS)["domain"],
            "gmail.com"
        )
        self.assertEqual(
            pymailcheck.suggest("test@comcast.nry", DOMAINS)["domain"],
            "comcast.net"
        )
        self.assertEqual(
            pymailcheck.suggest(
                "test@homail.con",
                DOMAINS,
                SECOND_LEVEL_DOMAINS,
                TOP_LEVEL_DOMAINS
            )["domain"],
            "hotmail.com"
        )
        self.assertEqual(
            pymailcheck.suggest(
                "test@hotmail.co",
                DOMAINS,
                SECOND_LEVEL_DOMAINS,
                TOP_LEVEL_DOMAINS
            )["domain"],
            "hotmail.com"
        )
        self.assertEqual(
            pymailcheck.suggest(
                "test@yajoo.com",
                DOMAINS,
                SECOND_LEVEL_DOMAINS,
                TOP_LEVEL_DOMAINS
            )["domain"],
            "yahoo.com"
        )
        self.assertEqual(
            pymailcheck.suggest(
                "test@randomsmallcompany.cmo",
                DOMAINS,
                SECOND_LEVEL_DOMAINS,
                TOP_LEVEL_DOMAINS
            )["domain"],
            "randomsmallcompany.com"
        )

    def test_idempotent_suggestions(self):
        self.assertEqual(
            pymailcheck.suggest(
                "test@yahooo.cmo",
                DOMAINS,
                SECOND_LEVEL_DOMAINS,
                TOP_LEVEL_DOMAINS
            )["domain"],
            "yahoo.com"
        )

    def test_no_suggestions_valid_2ld_tld(self):
        self.assertFalse(
            pymailcheck.suggest(
                "test@yahoo.co.uk",
                DOMAINS,
                SECOND_LEVEL_DOMAINS,
                TOP_LEVEL_DOMAINS
            )
        )

    def test_no_suggestions_valid_2ld_tld_close_domain(self):
        self.assertFalse(
            pymailcheck.suggest(
                "test@gmx.fr",
                DOMAINS,
                SECOND_LEVEL_DOMAINS,
                TOP_LEVEL_DOMAINS
            )
        )
