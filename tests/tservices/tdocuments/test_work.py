import unittest

from services.documents.all import Chapter, Page, Work


class TestWork(unittest.TestCase):

    def test_json(self):
        p1 = Page(bytes("abc", "utf-8"), "jpg")
        p2 = Page(bytes("cba", "utf-8"), "png")
        p3 = Page(bytes("xyz", "utf-8"), "png")
        p4 = Page(bytes("zyx", "utf-8"), "jpg")

        c1 = Chapter("CH1", [p1, p2])
        c2 = Chapter("CH2", [p3, p4])

        w1 = Work("Title", "Author", [c1, c2])
        wj = w1.to_json()
        w2 = Work.from_json(wj)

        self.assertEqual(w2.to_json(), wj)
        self.assertEqual(w1, w2)
