from __future__ import annotations
from dataclasses import dataclass
import json
from typing import List

from services.documents.c_chapter import CChapter
from services.documents.document import Document


@dataclass
class CWork(Document):
    title: str
    author: str
    chapters: List[CChapter]

    @classmethod
    def from_json(
        cls,
        data: str
    ) -> CWork:
        d = json.loads(data)
        title = d["title"]
        author = d["author"]
        chapters = [CChapter.from_json(json.dumps(x)) for x in d["chapters"]]
        return cls(title, author, chapters)
