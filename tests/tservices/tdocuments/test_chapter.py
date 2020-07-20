import unittest

from services.documents.all import Chapter, Page


class TestChapter(unittest.TestCase):

    def test_json(self):
        p1 = Page(bytes("abc", "utf-8"), "jpg")
        p2 = Page(bytes("cba", "utf-8"), "png")

        c1 = Chapter("CH1", [p1, p2])
        cj = c1.to_json()
        c2 = Chapter.from_json(cj)

        self.assertEqual(c2.to_json(), cj)
        self.assertEqual(c1, c2)
