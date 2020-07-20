from __future__ import annotations
import base64
from dataclasses import dataclass
import json

from services.documents.document import Document


@dataclass
class Page(Document):
    raw_data: bytes
    extension: str

    @classmethod
    def from_json(
        cls,
        data: str
    ) -> Page:
        d = json.loads(data)
        raw_data = base64.b64decode(d["raw_data"])
        extension = d["extension"]
        return cls(raw_data, extension)
