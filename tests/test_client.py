#!/usr/bin/env python3
import unittest
import requests

from snldata import client as snldata


class TestSnlData(unittest.TestCase):

    def setUp(self):
        self.service = snldata.SnlSession()
        super().setUp()

    def tearDown(self):
        self.service.close()

    def test_not_implemented_error(self):
        with self.assertRaises(Exception) as context:
            self.G = requests.Session(requests_session=False)
        
        self.assertTrue(NotImplementedError())

    def test_simplereq(self):
        self.G = requests.Session()
        self.test = self.G.get("https://snl.no/api/v1/search?query=")
        self.assertEqual(self.test.status_code, 200)

    def test_simplereq_dsd(self):
        self.G = requests.Session()
        self.test = self.G.get("https://denstoredanske.lex.dk/api/v1/search?query=")
        self.assertEqual(self.test.status_code, 200)

    def test_query(self):
        self.service.search(query="TCP", best=True)
        self.assertEqual(self.service.title, "TCP")

    def test_query_dsd(self):
        self.service.search(zone='dsd', query="februar", best=True)
        self.assertEqual(self.service.title, "februar")

    def test_query_zero_result(self):
        self.service.search(query="asdasdadadsasdasdasd", best=True)
        self.assertEqual(self.service.json, {})

    def test_query_zero_result_dsd(self):
        self.service.search(zone='dsd', query="asdasdadadsasdasdasd", best=True)
        self.assertEqual(self.service.json, {})

    # API endpoint removed
    # def test_query2(self):
    #     self.service.searchV2(
    #         {"encyclopedia": "snl", "query": "TCP", "limit": 3, "offset": 0},
    #         zone="prototyping", best=True)
    #     self.assertEqual(self.service.title, "TCP")

    # API endpoint removed
    # def test_query2_dsd(self):
    #     self.service.searchV2(
    #         {"encyclopedia": "dsd", "query": "februar", "limit": 3, "offset": 0},
    #         zone="prototyping", best=True)
    #     self.assertEqual(self.service.title, "februar")

    # API endpoint removed
    # def test_query_sml(self):
    #     self.service.searchV2(
    #         {"encyclopedia": "sml", "query": "CRISPR", "limit": 3, "offset": 0},
    #         zone="prototyping", best=True)
    #     self.assertEqual(self.service.title, "CRISPR")

    # API endpoint removed
    # def test_query_pd(self):
    #     self.service.searchV2(
    #         {"encyclopedia": "pd", "query": "Lækat", "limit": 3, "offset": 0},
    #         zone="prototyping-lex", best=True)
    #     self.assertEqual(self.service.title, "Lækat")

    def test_search(self):
        self.service.search(query="NTNU")
        self.service._get(1)
        self.assertEqual(self.service.title, "NTNU Universitetsbiblioteket")

    def test_search_no_result(self):
        self.service.search(query="asdasdadadsasdasdasd")
        self.service._get(0)
        self.assertEqual(self.service.json, {})

    def test_search_no_result_and_get(self):
        self.service.search(query="asdasdadadsasdasdasd")
        self.assertEqual(self.service.json, {})

    def test_search_fail(self):
        with self.assertRaises(Exception) as context:
            self.service.search(query="NTNU", limit=0)

            self.assertTrue(
            "Something went wrong with the parameters!" in
            str(context.exception))

    def test_search_fail_dsd(self):
        with self.assertRaises(Exception) as context:
            self.service.search(zone='dsd2', query="NTNU", limit=11)

        self.assertTrue(
            "Something went wrong with the parameters!" in
            str(context.exception))

    # API endpoint removed
    # def test_search2(self):
    #     self.service.searchV2(
    #         {"encyclopedia": "snl", "query": "NTNU", "limit": 3, "offset": 0},
    #         zone="prototyping")
    #     self.service._get(1)
    #     self.assertEqual(self.service.title, "NTNU Universitetsbiblioteket")

    # API endpoint removed
    # def test_search2_fail(self):
    #     with self.assertRaises(Exception) as context:
    #         self.service.searchV2(
    #             {"encyclopedia": "snl", "query": "NTNU", "limit": 0,
    #                 "offset": 5}, zone="prototyping")

    #     self.assertTrue(
    #         "Something went wrong with the parametres!" in
    #         str(context.exception))

    def test_alot_of_serch(self):
        self.service.search(query="Norge")
        self.service.search(query="Ole Bull")
        self.service._get(1)
        self.service.search(query="NTNU")
        self.service._get(1)
        self.assertEqual(self.service.title, "NTNU Universitetsbiblioteket")

    def test_garbagecontrol(self):
        self.service.search(query="Dr. Dre", best=True)
        self.service.search(query="Ole Ivars", best=True)
        self.assertRaises(AttributeError, lambda: self.service.gender)

if __name__ == '__main__':
    unittest.main()
