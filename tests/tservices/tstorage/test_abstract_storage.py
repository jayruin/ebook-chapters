from abc import ABC, abstractmethod
import json

from services.documents.all import (
    Catalog, CChapter, CWork, Chapter, MiscFile, Page, Work)
from services.storage.all import StorageError


class TestAbstractStorage(ABC):

    @classmethod
    def setUpClass(cls):
        json_file = "./tests/tservices/tstorage/config.json"
        with open(json_file, "r") as f:
            cls.config = json.loads(f.read())

    @abstractmethod
    def setUp(self):
        pass

    @abstractmethod
    def tearDown(self):
        pass

    def test_reset(self):
        p1 = Page(bytes("abc", "utf-8"), "jpg")
        p2 = Page(bytes("cba", "utf-8"), "png")
        p3 = Page(bytes("zyx", "utf-8"), "png")
        p4 = Page(bytes("xyz", "utf-8"), "jpg")
        p5 = Page(bytes("zzz", "utf-8"), "jpg")

        c1 = Chapter("CH1", [p1, p2])
        c2 = Chapter("CH2", [p3, p4, p5])

        title = "Title"
        author = "Author"
        w1 = Work(title, author, [c1, c2])

        self.storage.add_works([w1])

        self.storage.reset()

        w2 = self.storage.get_work(title, author)
        self.assertIsNone(w2)

    def test_populate_get_catalog(self):
        p1 = Page(bytes("abc", "utf-8"), "jpg")
        p2 = Page(bytes("cba", "utf-8"), "png")
        p3 = Page(bytes("zyx", "utf-8"), "png")
        p4 = Page(bytes("xyz", "utf-8"), "jpg")
        p5 = Page(bytes("zzz", "utf-8"), "jpg")

        c1 = Chapter("CH1", [p1, p2])
        c2 = Chapter("CH2", [p3, p4, p5])

        title = "Title"
        author = "Author"
        w1 = Work(title, author, [c1, c2])

        self.storage.add_works([w1])

        cc1 = CChapter("CH1", 2)
        cc2 = CChapter("CH2", 3)
        cw1 = CWork(title, author, [cc1, cc2])
        catalog = Catalog([cw1])

        self.assertEqual(catalog, self.storage.get_catalog())

    def test_work_add_get(self):
        p1 = Page(bytes("abc", "utf-8"), "jpg")
        p2 = Page(bytes("cba", "utf-8"), "png")
        p3 = Page(bytes("zyx", "utf-8"), "png")
        p4 = Page(bytes("xyz", "utf-8"), "jpg")
        p5 = Page(bytes("zzz", "utf-8"), "jpg")

        c1 = Chapter("CH1", [p1, p2])
        c2 = Chapter("CH2", [p3, p4, p5])

        title = "Title"
        author = "Author"
        w1 = Work(title, author, [c1, c2])

        self.storage.add_works([w1])

        w2 = self.storage.get_work(title, author)
        self.assertEqual(w1, w2)

    def test_add_duplicate_work(self):
        p1 = Page(bytes("abc", "utf-8"), "jpg")
        p2 = Page(bytes("cba", "utf-8"), "png")
        p3 = Page(bytes("zyx", "utf-8"), "png")
        p4 = Page(bytes("xyz", "utf-8"), "jpg")
        p5 = Page(bytes("zzz", "utf-8"), "jpg")

        c1 = Chapter("CH1", [p1, p2])
        c2 = Chapter("CH2", [p3, p4, p5])

        title = "Title"
        author = "Author"
        w1 = Work(title, author, [c1, c2])

        self.storage.add_works([w1])

        with self.assertRaises(StorageError):
            self.storage.add_works([w1])

    def test_chapter_add_get(self):
        p1 = Page(bytes("abc", "utf-8"), "jpg")
        p2 = Page(bytes("cba", "utf-8"), "png")
        p3 = Page(bytes("zyx", "utf-8"), "png")
        p4 = Page(bytes("xyz", "utf-8"), "jpg")
        p5 = Page(bytes("zzz", "utf-8"), "jpg")

        chapter_title = "Only Chapter"
        c1 = Chapter(chapter_title, [p1, p2, p3, p4, p5])

        title = "Title"
        author = "Author"

        self.storage.new_work(title, author)
        self.storage.add_chapters(title, author, [c1])

        c2 = self.storage.get_chapter(title, author, chapter_title)
        self.assertEqual(c1, c2)

    def test_chapter_add_no_work(self):
        p1 = Page(bytes("abc", "utf-8"), "jpg")
        p2 = Page(bytes("cba", "utf-8"), "png")
        p3 = Page(bytes("zyx", "utf-8"), "png")
        p4 = Page(bytes("xyz", "utf-8"), "jpg")
        p5 = Page(bytes("zzz", "utf-8"), "jpg")

        chapter_title = "Only Chapter"
        c1 = Chapter(chapter_title, [p1, p2, p3, p4, p5])

        title = "Title"
        author = "Author"

        with self.assertRaises(StorageError):
            self.storage.add_chapters(title, author, [c1])

    def test_get_nonexistent_work(self):
        w1 = self.storage.get_work("title", "author")
        self.assertIsNone(w1)

    def test_get_nonexistent_chapter(self):
        c1 = self.storage.get_chapter("title", "author", "chaptertitle")
        self.assertIsNone(c1)

    def test_contains_work_no_chapter(self):
        title = "Work With No Chapters"
        author = "Author"

        w1 = Work(title, author, [])

        self.storage.add_works([w1])

        contains = self.storage.contains_work(title, author)
        self.assertTrue(contains)

    def test_contains_work_chapter_no_page(self):
        title = "Work With Chapters"
        author = "Author"

        chapter_title = "Chapter With No Pages"

        w = Work(title, author, [Chapter(chapter_title, [])])

        self.storage.add_works([w])

        contains = self.storage.contains_chapter(title, author, chapter_title)
        self.assertTrue(contains)

    def test_add_chapter_to_work_twice(self):
        p1 = Page(bytes("abc", "utf-8"), "jpg")
        p2 = Page(bytes("cba", "utf-8"), "png")
        p3 = Page(bytes("zyx", "utf-8"), "png")
        p4 = Page(bytes("xyz", "utf-8"), "jpg")
        p5 = Page(bytes("zzz", "utf-8"), "jpg")

        c1 = Chapter("ZZZ", [p1, p2])
        c2 = Chapter("AAA", [p3, p4, p5])

        title = "Title"
        author = "Author"

        w1 = Work(title, author, [c1, c2])
        self.storage.new_work(title, author)
        self.storage.add_chapters(title, author, [c1])
        self.storage.add_chapters(title, author, [c2])

        w2 = self.storage.get_work(title, author)
        self.assertEqual(w1, w2)

    def test_misc_file(self):
        f1 = MiscFile("abc", bytes("abc", "utf-8"))
        f2 = MiscFile("xyz", bytes("xyz", "utf-8"))

        self.storage.add_misc_files([f1, f2])

        self.assertTrue(self.storage.contains_misc_file("abc"))
        self.assertFalse(self.storage.contains_misc_file("abcxyz"))
        self.assertEqual(f2, self.storage.get_misc_file("xyz"))
        set1 = {"abc", "xyz"}
        set2 = self.storage.get_all_misc_file_names()
        self.assertEqual(set1, set2)
