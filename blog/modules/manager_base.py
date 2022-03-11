import hashlib


class ManagerBase:
    def __init__(self) -> None:
        self._md5 = hashlib.md5()

    def _calc_hash(self, content: str) -> str:
        md5 = self._md5
        md5.update(content.encode('utf-8'))
        return md5.hexdigest()

    def _get_text_content(self, file: str) -> str:
        with open(file, mode='r', encoding="utf8") as f:
            content = f.read()
        return content
