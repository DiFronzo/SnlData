#!/usr/bin/env python3
import unittest
# import pytest
import requests

from snldata import client as snldata


class TestSnlData(unittest.TestCase):

    def setUp(self):
        self.service = snldata.SnlSession()
        super().setUp()

    def tearDown(self):
        self.service.close()

    def test_simplereq(self):
        self.G = requests.Session()
        self.test = self.G.get("https://snl.no/api/v1/search?query=")
        self.assertEqual(self.test.status_code, 200)

    def test_query(self):
        self.service.search(query="aa-", best=True)
        self.assertEqual(self.service.title, "aa-")

    def test_query2(self):
        self.service.searchV2(
            {"encyclopedia": "snl", "query": "aa-", "limit": 3, "offset": 0},
            zone="prototyping", best=True)
        self.assertEqual(self.service.title, "aa-")

    def test_search(self):
        self.service.search(query="NTNU")
        self.service._get(1)
        self.assertEqual(self.service.title, "NTNU Universitetsbiblioteket")

    def test_search_fail(self):
        with self.assertRaises(Exception) as context:
            self.service.search(query="NTNU", limit=0)

        self.assertTrue(
            "Something went wrong with the parametres!" in
            str(context.exception))

    def test_search2(self):
        self.service.searchV2(
            {"encyclopedia": "snl", "query": "NTNU", "limit": 3, "offset": 0},
            zone="prototyping")
        self.service._get(1)
        self.assertEqual(self.service.title, "NTNU Universitetsbiblioteket")

    def test_search2_fail(self):
        with self.assertRaises(Exception) as context:
            self.service.searchV2(
                {"encyclopedia": "snl", "query": "NTNU", "limit": 0,
                    "offset": 5}, zone="prototyping")

        self.assertTrue(
            "Something went wrong with the parametres!" in
            str(context.exception))

    def test_garbagecontrol(self):
        self.service.search(query="Dr. Dre", best=True)
        self.service.search(query="Ole Ivars", best=True)
        self.assertRaises(AttributeError, lambda: self.service.gender)

if __name__ == '__main__':
    unittest.main()
