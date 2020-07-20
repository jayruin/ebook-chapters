from html.parser import HTMLParser
from typing import List, Tuple


class BaseParser(HTMLParser):

    def __init__(
        self
    ) -> None:
        super(BaseParser, self).__init__(convert_charrefs=True)

        self.buffer: str = ""

    def get_buffer(
        self
    ) -> str:
        result = self.buffer
        self.buffer = ""
        self.reset()
        return result

    @staticmethod
    def _get_attrs_str(
        attrs: List[Tuple[str, str]]
    ) -> str:
        attrs_str = " ".join(["{0}=\"{1}\"".format(*attr) for attr in attrs])
        if attrs_str:
            attrs_str = " " + attrs_str
        return attrs_str
