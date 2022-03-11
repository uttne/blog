from html.parser import HTMLParser
from .blog_metadata import BlogMetadata


class PostHTMLParser(HTMLParser):
    def __init__(self, *, convert_charrefs: bool = ...) -> None:
        self._blogMetadata = BlogMetadata()
        super().__init__(convert_charrefs=convert_charrefs)

    def handle_comment(self, data: str) -> None:
        lines = [l for l in data.splitlines() if 0 < len(l)]
        if(len(lines) == 0):
            return
        first = lines[0].strip(' ').lower()
        if(first != "blog-meta-data"):
            return

        for l in lines[1:]:
            keyValue = l.split(':', 1)
            key = keyValue[0].strip(' ').lower()
            value = keyValue[-1].strip(' ')
            match key:
                case "title":
                    self._blogMetadata.title = value
                case "tags":
                    self._blogMetadata.tags = [v for v in [
                        v.strip(' ') for v in value.split(",")] if v != ""]
                case "hash":
                    self._blogMetadata.hash = value

    def get_blog_metadata(self) -> BlogMetadata:
        return self._blogMetadata
