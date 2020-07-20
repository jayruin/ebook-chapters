from __future__ import annotations
import base64
from dataclasses import dataclass
import json

from services.documents.document import Document


@dataclass
class MiscFile(Document):
    file_name: str
    raw_data: bytes

    @classmethod
    def from_json(
        cls,
        data: str
    ) -> MiscFile:
        d = json.loads(data)
        file_name = d["file_name"]
        raw_data = base64.b64decode(d["raw_data"])
        return cls(file_name, raw_data)
