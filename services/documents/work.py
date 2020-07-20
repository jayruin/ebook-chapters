from __future__ import annotations
from dataclasses import dataclass
import json
from typing import List

from services.documents.chapter import Chapter
from services.documents.document import Document


@dataclass
class Work(Document):
    title: str
    author: str
    chapters: List[Chapter]

    @classmethod
    def from_json(
        cls,
        data: str
    ) -> Work:
        d = json.loads(data)
        title = d["title"]
        author = d["author"]
        chapters = [Chapter.from_json(json.dumps(x)) for x in d["chapters"]]
        return cls(title, author, chapters)
