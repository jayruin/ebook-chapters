import unittest

from services.documents.all import Catalog, CChapter, CWork


class TestCatalog(unittest.TestCase):

    def test_json(self):
        c1 = CChapter("CH1", 2)
        c2 = CChapter("CH2", 3)
        c3 = CChapter("Chapter 1", 5)
        c4 = CChapter("Chapter 2", 7)

        work1_title = "Title"
        work1_author = "Author"
        work2_title = "not a title"
        work2_author = "not an author"
        w1 = CWork(work1_title, work1_author, [c1, c2])
        w2 = CWork(work2_title, work2_author, [c3, c4])

        catalog1 = Catalog([w1, w2])
        catalog_json = catalog1.to_json()
        catalog2 = Catalog.from_json(catalog_json)
        self.assertEqual(catalog1, catalog2)
