from __future__ import annotations
from abc import ABC, abstractmethod
from typing import List, Optional, Set

from services.documents.all import Catalog, Chapter, MiscFile, Work


class AbstractStorage(ABC):

    @abstractmethod
    def reset(
        self
    ) -> None:
        pass

    @abstractmethod
    def get_catalog(
        self,
    ) -> Catalog:
        pass

    @abstractmethod
    def contains_work(
        self,
        title: str,
        author: str
    ) -> bool:
        pass

    @abstractmethod
    def contains_chapter(
        self,
        title: str,
        author: str,
        chapter_title: str
    ) -> bool:
        pass

    @abstractmethod
    def get_work(
        self,
        title: str,
        author: str
    ) -> Optional[Work]:
        pass

    @abstractmethod
    def get_chapter(
        self,
        title: str,
        author: str,
        chapter_title: str
    ) -> Optional[Chapter]:
        pass

    @abstractmethod
    def new_work(
        self,
        title: str,
        author: str
    ) -> None:
        pass

    @abstractmethod
    def add_works(
        self,
        works: List[Work]
    ) -> None:
        pass

    @abstractmethod
    def add_chapters(
        self,
        title: str,
        author: str,
        chapters: List[Chapter]
    ) -> None:
        pass

    @abstractmethod
    def get_misc_file(
        self,
        file_name: str
    ) -> Optional[MiscFile]:
        pass

    @abstractmethod
    def add_misc_files(
        self,
        misc_files: List[MiscFile]
    ) -> None:
        pass

    @abstractmethod
    def contains_misc_file(
        self,
        file_name: str
    ) -> bool:
        pass

    @abstractmethod
    def get_all_misc_file_names(
        self
    ) -> Set[str]:
        pass

    def import_new_content(
        self,
        other: AbstractStorage
    ) -> None:
        for c_work in other.get_catalog().works:
            title = c_work.title
            author = c_work.author
            if not self.contains_work(title, author):
                self.add_works([other.get_work(title, author)])
                continue
            for c_chapter in c_work.chapters:
                chapter_title = c_chapter.chapter_title
                if not self.contains_chapter(title, author, chapter_title):
                    chapter = other.get_chapter(title, author, chapter_title)
                    self.add_chapters(title, author, [chapter])
        self.add_misc_files([
            other.get_misc_file(misc_file_name)
            for misc_file_name in other.get_all_misc_file_names()
        ])
