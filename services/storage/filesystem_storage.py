import json
import math
import os
from pathlib import Path
import shutil
from typing import Any, Callable, Generator, List, Optional, Set

from services.documents.all import (
    Catalog, CChapter, CWork, Chapter, MiscFile, Page, Work
)
from services.storage.abstract_storage import AbstractStorage
from services.storage.exceptions import StorageError


class FilesystemStorage(AbstractStorage):
    def __init__(
        self,
        root_directory: str,
        misc_directory: str
    ) -> None:
        self._root_path: Path = Path(root_directory)
        self._misc_path: Path = Path(misc_directory)
        self._filesystem_init()

    def reset(
        self
    ) -> None:
        self._filesystem_destroy()
        self._filesystem_init()

    def get_catalog(
        self
    ) -> Catalog:
        works = []
        for entry_author in self._scandir(self._root_path, self._f_dir):
            author_path = self._root_path.joinpath(entry_author.name)
            for entry_title in self._scandir(author_path, self._f_dir):
                chapters = []
                title_path = author_path.joinpath(entry_title.name)
                for entry_chapter in self._scandir(title_path, self._f_dir):
                    chapter_path = title_path.joinpath(entry_chapter.name)
                    generator = self._scandir(chapter_path, self._f_not_config)
                    page_count = len(list(generator))
                    c_chapter = CChapter(entry_chapter.name, page_count)
                    chapters.append(c_chapter)
                c_work = CWork(entry_title.name, entry_author.name, chapters)
                works.append(c_work)
        return Catalog(works)

    def contains_work(
        self,
        title: str,
        author: str
    ) -> bool:
        work_path = self._root_path.joinpath(author, title)
        return work_path.exists() and work_path.is_dir()

    def contains_chapter(
        self,
        title: str,
        author: str,
        chapter_title: str
    ) -> bool:
        chapter_path = self._root_path.joinpath(author, title, chapter_title)
        return chapter_path.exists() and chapter_path.is_dir()

    def get_work(
        self,
        title: str,
        author: str
    ) -> Optional[Work]:
        if not self.contains_work(title, author):
            return None
        chapters = [
            self.get_chapter(title, author, chapter_title)
            for chapter_title in self._get_chapter_order(title, author)
        ]
        return Work(title, author, chapters)

    def get_chapter(
        self,
        title: str,
        author: str,
        chapter_title: str
    ) -> Optional[Chapter]:
        if not self.contains_chapter(title, author, chapter_title):
            return None
        chapter_path = self._root_path.joinpath(author, title, chapter_title)
        pages = []
        entries = list(self._scandir(chapter_path))
        entries.sort(key=lambda x: x.name)
        for entry in entries:
            with open(entry, "rb") as f:
                raw_data = f.read()
                extension = Path(entry.path).suffix[1:]
                pages.append(Page(raw_data, extension))
        return Chapter(chapter_title, pages)

    def new_work(
        self,
        title: str,
        author: str
    ) -> None:
        work_path = self._root_path.joinpath(author, title)
        if work_path.exists():
            raise StorageError
        os.makedirs(work_path)

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
        if not self.contains_work(title, author):
            raise StorageError
        for chapter in chapters:
            if self.contains_chapter(title, author, chapter.chapter_title):
                raise StorageError
        chapter_order = self._get_chapter_order(title, author)
        work_path = self._root_path.joinpath(author, title)
        for chapter in chapters:
            chapter_path = work_path.joinpath(chapter.chapter_title)
            os.makedirs(chapter_path)
            if not chapter.pages:
                return
            digits = int(math.log10(len(chapter.pages))) + 1
            for index, page in enumerate(chapter.pages, start=1):
                file_name = f"{str(index).zfill(digits)}.{page.extension}"
                file_path = chapter_path.joinpath(file_name)
                with open(file_path, "wb") as f:
                    f.write(page.raw_data)
            chapter_order.append(chapter.chapter_title)
        self._save_chapter_order(title, author, chapter_order)

    def get_misc_file(
        self,
        file_name: str
    ) -> Optional[MiscFile]:
        if not self.contains_misc_file(file_name):
            return None
        with open(Path(self._misc_path, file_name), "rb") as f:
            return MiscFile(file_name, f.read())

    def add_misc_files(
        self,
        misc_files: List[MiscFile]
    ) -> None:
        for misc_file in misc_files:
            file_path = Path(self._misc_path, misc_file.file_name)
            if file_path.exists():
                raise StorageError
            with open(file_path, "wb") as f:
                f.write(misc_file.raw_data)

    def contains_misc_file(
        self,
        file_name: str
    ) -> bool:
        return Path(self._misc_path, file_name).exists()

    def get_all_misc_file_names(
            self
    ) -> Set[str]:
        file_names = set()
        for entry in self._scandir(Path(self._misc_path)):
            file_names.add(entry.name)
        return file_names

    def _filesystem_init(
        self
    ) -> None:
        if not self._root_path.exists():
            os.makedirs(self._root_path)
        if not self._misc_path.exists():
            os.makedirs(self._misc_path)

    def _filesystem_destroy(
        self
    ) -> None:
        for entry in self._scandir(self._root_path, self._f_dir):
            shutil.rmtree(entry.path)
        for entry in self._scandir(self._misc_path, self._f_dir):
            shutil.rmtree(entry.path)

    def _get_chapter_order(
        self,
        title: str,
        author: str
    ) -> List[str]:
        chapters = None
        work_path = self._root_path.joinpath(author, title)
        order_file_path = work_path.joinpath("order.json")
        if order_file_path.exists() and order_file_path.is_file():
            with open(order_file_path, "r") as f:
                chapters = json.loads(f.read())["order"]
        else:
            chapters = [
                entry.name
                for entry in self._scandir(work_path, self._f_dir)
            ]
        return chapters

    def _save_chapter_order(
        self,
        title: str,
        author: str,
        chapter_order: List[str]
    ) -> None:
        work_path = self._root_path.joinpath(author, title)
        order_file_path = work_path.joinpath("order.json")
        with open(order_file_path, "w") as f:
            f.write(json.dumps({"order": chapter_order}, indent=4))

    @staticmethod
    def _scandir(
        path: Path,
        filter_function: Optional[Callable[[os.DirEntry], bool]] = None
    ) -> Generator[os.DirEntry, None, None]:
        with os.scandir(path) as it:
            for entry in it:
                if not filter_function or filter_function(entry):
                    yield entry

    @staticmethod
    def _f_dir(
        entry: os.DirEntry
    ) -> bool:
        return entry.is_dir()

    @staticmethod
    def _f_not_config(
        entry: os.DirEntry
    ) -> bool:
        return not entry.name.endswith(".json")
