from __future__ import annotations
from dataclasses import dataclass
import json
from typing import List

from services.documents.c_work import CWork
from services.documents.document import Document


@dataclass
class Catalog(Document):
    works: List[CWork]

    @classmethod
    def from_json(
        cls,
        data: str
    ) -> Catalog:
        d = json.loads(data)
        works = [CWork.from_json(json.dumps(x)) for x in d["works"]]
        return cls(works)

    def get_work(
        self,
        title: str,
        author: str
    ) -> CWork:
        for work in self.works:
            if work.title == title and work.author == author:
                return work
