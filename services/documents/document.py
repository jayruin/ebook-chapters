from __future__ import annotations
from abc import ABC, abstractmethod
import base64
import json
from typing import Any, Dict, Union


class Document(ABC):

    @classmethod
    @abstractmethod
    def from_json(
        cls,
        data: str
    ) -> Document:
        pass

    def to_json(
        self
    ) -> str:
        return json.dumps(self, default=self.serialize, indent=4)

    @staticmethod
    def serialize(
        o: Any
    ) -> Union[str, Dict[str, Any]]:
        if isinstance(o, bytes):
            return base64.b64encode(o).decode("utf-8")
        else:
            return vars(o)

    def __eq__(
        self,
        other: Any
    ) -> bool:
        if not isinstance(other, Document):
            return False
        return vars(self) == vars(other)
