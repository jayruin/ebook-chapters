from __future__ import annotations
from dataclasses import dataclass
import json

from services.documents.document import Document


@dataclass
class CChapter(Document):
    chapter_title: str
    number_of_pages: int

    @classmethod
    def from_json(
        cls,
        data: str
    ) -> CChapter:
        d = json.loads(data)
        return cls(**d)
