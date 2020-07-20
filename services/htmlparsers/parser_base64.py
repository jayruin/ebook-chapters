import base64
import mimetypes
from pathlib import Path
from typing import Dict, List, Tuple

from services.htmlparsers.parser_copy import ParserCopy


class ParserBase64(ParserCopy):

    def __init__(
        self,
    ) -> None:
        super(ParserBase64, self).__init__()
        self._file_mappings: Dict[str, bytes] = {}

    def add_file_mapping(
        self,
        file_name: str,
        raw_data: bytes
    ) -> None:
        self._file_mappings[file_name] = raw_data

    def handle_starttag(
        self,
        tag: str,
        attrs: List[Tuple[str, str]]
    ) -> None:
        modified_attrs = []
        for attr in attrs:
            name, value = attr
            if ((tag == "link" and name == "href" and value.endswith(".css"))
                    or (tag == "img" and name == "src")):
                modified_attrs.append(self._base64_encode(attr))
            else:
                modified_attrs.append(attr)
        super(ParserBase64, self).handle_starttag(tag, modified_attrs)

    def handle_startendtag(
        self,
        tag: str,
        attrs: List[Tuple[str, str]]
    ) -> None:
        self.buffer += f"<{tag}{self._get_attrs_str(attrs)} />"

    def _base64_encode(
        self,
        attr: Tuple[str, str]
    ) -> Tuple[str, str]:
        file_name = Path(attr[1]).name
        if file_name not in self._file_mappings:
            return attr
        data_url = f"data:{mimetypes.guess_type(file_name)[0]};base64,"
        raw_data = self._file_mappings[file_name]
        data_url += base64.b64encode(raw_data).decode("utf-8")
        return attr[0], data_url
