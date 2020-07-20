from typing import List, Tuple

from services.htmlparsers.base_parser import BaseParser


class ParserCopy(BaseParser):

    def handle_starttag(
        self,
        tag: str,
        attrs: List[Tuple[str, str]]
    ) -> None:
        self.buffer += f"<{tag}{self._get_attrs_str(attrs)}>"

    def handle_endtag(
        self,
        tag: str
    ) -> None:
        self.buffer += f"</{tag}>"

    def handle_startendtag(
        self,
        tag: str,
        attrs: List[Tuple[str, str]]
    ) -> None:
        self.buffer += f"<{tag}{self._get_attrs_str(attrs)} />"

    def handle_data(
        self,
        data: str
    ) -> None:
        self.buffer += data

    def handle_decl(
        self,
        decl: str
    ) -> None:
        self.buffer += f"<!{decl}>"
