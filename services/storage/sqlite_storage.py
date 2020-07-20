from collections import defaultdict
import sqlite3
from typing import List, Optional, Set

from services.documents.all import (
    Catalog, CChapter, CWork, Chapter, MiscFile, Page, Work
)
from services.storage.abstract_storage import AbstractStorage
from services.storage.exceptions import StorageError


class SqliteStorage(AbstractStorage):
    def __init__(
        self,
        connection_string: str,
        init_script: str,
        destroy_script: str
    ) -> None:
        self._connection_string: str = connection_string
        self._init_script: str = init_script
        self._destroy_script: str = destroy_script
        self._sql_init()

    def reset(
        self
    ) -> None:
        self._sql_destroy()
        self._sql_init()

    def get_catalog(
        self
    ) -> Catalog:
        works = []
        catalog_dict = defaultdict(list)
        conn = sqlite3.connect(self._connection_string)
        query = (
            "SELECT *"
            " FROM CatalogView"
        )
        for row in conn.execute(query):
            key = (row[0], row[1])
            value = CChapter(row[2], row[3])
            catalog_dict[key].append(value)
        conn.close()
        for k, v in catalog_dict.items():
            works.append(CWork(k[0], k[1], v))
        return Catalog(works)

    def contains_work(
        self,
        title: str,
        author: str
    ) -> bool:
        result = False
        conn = sqlite3.connect(self._connection_string)
        conn.row_factory = sqlite3.Row
        cur = conn.cursor()
        query = (
            "SELECT *"
            " FROM CatalogView"
            " WHERE title=? AND author=?"
        )
        cur.execute(query, (title, author))
        result = cur.fetchone() is not None
        conn.close()
        return result

    def contains_chapter(
        self,
        title: str,
        author: str,
        chapter_title: str
    ) -> bool:
        result = False
        conn = sqlite3.connect(self._connection_string)
        conn.row_factory = sqlite3.Row
        cur = conn.cursor()
        query = (
            "SELECT *"
            " FROM CatalogView"
            " WHERE title=? AND author=? AND chaptertitle=?"
        )
        cur.execute(query, (title, author, chapter_title))
        result = cur.fetchone() is not None
        conn.close()
        return result

    def get_work(
        self,
        title: str,
        author: str
    ) -> Optional[Work]:
        if not self.contains_work(title, author):
            return None
        conn = sqlite3.connect(self._connection_string)
        conn.row_factory = sqlite3.Row
        current_chaptertitle = None
        chapters = []
        query = (
            "SELECT *"
            " FROM WorksView"
            " WHERE title=? AND author=?"
            " ORDER BY chapterindex ASC, pageindex ASC"
        )
        for row in conn.execute(query, (title, author)):
            if row["chaptertitle"] != current_chaptertitle:
                if current_chaptertitle is not None:
                    chapters.append(Chapter(current_chaptertitle, pages))
                current_chaptertitle = row["chaptertitle"]
                pages = []
            pages.append(Page(row["rawdata"], row["extension"]))

        chapters.append(Chapter(current_chaptertitle, pages))
        conn.close()
        return Work(title, author, chapters)

    def get_chapter(
        self,
        title: str,
        author: str,
        chapter_title: str
    ) -> Optional[Chapter]:
        if not self.contains_chapter(title, author, chapter_title):
            return None
        conn = sqlite3.connect(self._connection_string)
        conn.row_factory = sqlite3.Row
        pages = []
        query = (
            "SELECT *"
            " FROM WorksView"
            " WHERE title=? AND author=? AND chaptertitle=?"
            " ORDER BY pageindex ASC"
        )
        for row in conn.execute(query, (title, author, chapter_title)):
            pages.append(Page(row["rawdata"], row["extension"]))
        conn.close()
        return Chapter(chapter_title, pages)

    def new_work(
        self,
        title: str,
        author: str
    ) -> None:
        conn = sqlite3.connect(self._connection_string)
        conn.execute("PRAGMA foreign_keys=ON")
        cur = conn.cursor()
        try:
            query = (
                "INSERT INTO Works (title, author)"
                " VALUES (?, ?)"
            )
            cur.execute(query, (title, author))
            conn.commit()
        except sqlite3.IntegrityError:
            raise StorageError
        finally:
            conn.close()

    def add_works(
        self,
        works: List[Work]
    ) -> None:
        for work in works:
            self.new_work(work.title, work.author)
            self.add_chapters(work.title, work.author, work.chapters)

    def add_chapters(
        self,
        title: str,
        author: str,
        chapters: List[Chapter]
    ) -> None:
        workid = self._get_workid(title, author)
        conn = sqlite3.connect(self._connection_string)
        conn.execute("PRAGMA foreign_keys=ON")
        cur = conn.cursor()
        try:
            next_index = self._get_next_chapter_index(title, author)
            values = [
                (
                    workid,
                    chapter.chapter_title,
                    index
                )
                for index, chapter in enumerate(chapters, start=next_index)
            ]
            query = (
                "INSERT INTO Chapters (workid, chaptertitle, chapterindex)"
                " VALUES (?, ?, ?)"
            )
            cur.executemany(query, values)
            conn.commit()
            values = [
                (
                    self._get_chapterid(title, author, chapter.chapter_title),
                    page.raw_data,
                    page.extension,
                    page_index
                )
                for chapter in chapters
                for page_index, page in enumerate(chapter.pages, start=1)
            ]
            query = (
                "INSERT INTO Pages (chapterid, rawdata, extension, pageindex)"
                " VALUES (?, ?, ?, ?)"
            )
            cur.executemany(query, values)
            conn.commit()
        except sqlite3.IntegrityError:
            raise StorageError
        finally:
            conn.close()

    def get_misc_file(
        self,
        file_name: str
    ) -> Optional[MiscFile]:
        if not self.contains_misc_file(file_name):
            return None
        conn = sqlite3.connect(self._connection_string)
        conn.row_factory = sqlite3.Row
        query = (
            "SELECT *"
            " FROM MiscFiles"
            " WHERE filename=?"
        )
        raw_data = conn.execute(query, (file_name, )).fetchone()["rawdata"]
        conn.close()
        return MiscFile(file_name, raw_data)

    def add_misc_files(
        self,
        misc_files: List[MiscFile]
    ) -> None:
        conn = sqlite3.connect(self._connection_string)
        cur = conn.cursor()
        try:
            values = [
                (
                    misc_file.file_name,
                    misc_file.raw_data
                )
                for misc_file in misc_files
            ]
            query = (
                "INSERT INTO MiscFiles"
                " VALUES (?, ?)"
            )
            cur.executemany(query, values)
            conn.commit()
        except sqlite3.IntegrityError:
            raise StorageError
        finally:
            conn.close()

    def contains_misc_file(
        self,
        file_name: str
    ) -> bool:
        result = False
        conn = sqlite3.connect(self._connection_string)
        conn.row_factory = sqlite3.Row
        cur = conn.cursor()
        query = (
            "SELECT *"
            " FROM MiscFiles"
            " WHERE filename=?"
        )
        cur.execute(query, (file_name, ))
        result = cur.fetchone() is not None
        conn.close()
        return result

    def get_all_misc_file_names(
            self
    ) -> Set[str]:
        misc_file_names = set()
        conn = sqlite3.connect(self._connection_string)
        conn.row_factory = sqlite3.Row
        query = (
            "SELECT filename"
            " FROM MiscFiles"
        )
        for row in conn.execute(query):
            misc_file_names.add(row["filename"])
        conn.close()
        return misc_file_names

    def _sql_init(
        self
    ) -> None:
        conn = sqlite3.connect(self._connection_string)
        cur = conn.cursor()
        cur.executescript(self._init_script)
        conn.commit()
        conn.close()

    def _sql_destroy(
        self
    ) -> None:
        conn = sqlite3.connect(self._connection_string)
        cur = conn.cursor()
        cur.executescript(self._destroy_script)
        conn.commit()
        conn.close()

    def _get_next_chapter_index(
        self,
        title: str,
        author: str
    ) -> int:
        conn = sqlite3.connect(self._connection_string)
        cur = conn.cursor()
        query = (
            "SELECT MAX(chapterindex) + 1"
            " FROM CatalogView"
            " WHERE title=? AND author=?"
            " GROUP BY title, author"
        )
        cur.execute(query, (title, author))
        if row := cur.fetchone():
            result = row[0] or 0
            conn.close()
            return result
        else:
            conn.close()
            raise StorageError

    def _get_workid(
        self,
        title: str,
        author: str
    ) -> Optional[int]:
        conn = sqlite3.connect(self._connection_string)
        cur = conn.cursor()
        query = (
            "SELECT id"
            " FROM Works"
            " WHERE title=? AND author=?"
        )
        cur.execute(query, (title, author))
        if row := cur.fetchone():
            result = row[0]
        else:
            result = None
        conn.close()
        return result

    def _get_chapterid(
        self,
        title: str,
        author: str,
        chapter_title: str
    ) -> Optional[int]:
        conn = sqlite3.connect(self._connection_string)
        cur = conn.cursor()
        query = (
            "SELECT Chapters.id"
            " FROM Works"
            " INNER JOIN Chapters"
            " ON Works.id = Chapters.workid"
            " WHERE title=? AND author=? AND chaptertitle=?"
        )
        cur.execute(query, (title, author, chapter_title))
        if row := cur.fetchone():
            result = row[0]
        else:
            result = None
        conn.close()
        return result
