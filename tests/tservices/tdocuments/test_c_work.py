import unittest

from services.documents.all import CChapter, CWork


class TestCWork(unittest.TestCase):

    def test_json(self):
        c1 = CChapter("CH1", 2)
        c2 = CChapter("CH2", 2)

        w1 = CWork("Title", "Author", [c1, c2])
        wj = w1.to_json()
        w2 = CWork.from_json(wj)

        self.assertEqual(w2.to_json(), wj)
        self.assertEqual(w1, w2)
