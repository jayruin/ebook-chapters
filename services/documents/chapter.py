from __future__ import annotations
from dataclasses import dataclass
import json
from typing import List

from services.documents.document import Document
from services.documents.page import Page


@dataclass
class Chapter(Document):
    chapter_title: str
    pages: List[Page]

    @classmethod
    def from_json(
        cls,
        data: str
    ) -> Chapter:
        d = json.loads(data)
        chapter_title = d["chapter_title"]
        pages = [Page.from_json(json.dumps(x)) for x in d["pages"]]
        return cls(chapter_title, pages)
