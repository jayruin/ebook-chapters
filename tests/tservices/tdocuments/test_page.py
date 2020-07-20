import unittest

from services.documents.all import Page


class TestPage(unittest.TestCase):

    def test_json(self):
        p1 = Page(bytes("abc", "utf-8"), "jpg")
        pj = p1.to_json()
        p2 = Page.from_json(pj)

        self.assertEqual(p2.to_json(), pj)
        self.assertIsInstance(p2.raw_data, bytes)
        self.assertEqual(p1, p2)
