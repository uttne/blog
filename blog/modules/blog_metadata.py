
class BlogMetadata:
    def __init__(self, title: str = "", tags: list[str] = [], hash: str = "", is_draft: bool = False) -> None:
        self.title = title
        self.tags = tags
        self.hash = hash
        self.is_draft = is_draft
