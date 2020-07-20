import unittest

from services.documents.all import CChapter


class TestCChapter(unittest.TestCase):

    def test_json(self):
        c1 = CChapter("CH1", 2)
        cj = c1.to_json()
        c2 = CChapter.from_json(cj)

        self.assertEqual(c2.to_json(), cj)
        self.assertEqual(c1, c2)
