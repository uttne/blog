import os
import json
from .manager_base import ManagerBase
from .post_check_kind import PostCheckKind


class PostManager(ManagerBase):
    def __init__(self, postManagementFile="./posts.json", postGlobPattern="./posts/*.md") -> None:
        super().__init__()
        self._postManagementFile = postManagementFile
        self._postGlobPattern = postGlobPattern

    def _load(self):
        postManagementFile = self._postManagementFile

        if os.path.exists(postManagementFile):
            with open(postManagementFile, "r", encoding="utf-8") as f:
                contentJson = f.read()
                content = json.loads(contentJson)
                return content
        else:
            return {}

    def _save(self, posts):
        postManagementFile = self._postManagementFile

        contentJson = json.dumps(posts, indent=4)
        with open(postManagementFile, "w", encoding="utf-8") as f:
            f.write(contentJson)

    def get_num_key(self, file: str) -> str:
        fileName: str = os.path.basename(file)

        numStr = fileName.split("-", 1)[0]
        numKey = str(int(numStr))
        return numKey

    def check(self, file: str) -> PostCheckKind:

        numKey = self.get_num_key(file)

        posts = self._load()
        post = posts.get(numKey)
        if not post:
            return PostCheckKind.NEW

        content = self._get_text_content(file)
        localHash = self._calc_hash(content)

        localHashWithPosts = post.get("localHash")

        if localHash == localHashWithPosts:
            return PostCheckKind.NO_CHANGE
        else:
            return PostCheckKind.MODIFIED

    def get_post_id(self, file: str) -> str:

        numKey = self.get_num_key(file)

        posts = self._load()
        post = posts.get(numKey)
        return post["postId"]

    def update(self, file: str, localHash: str, postId: str) -> None:

        numKey = self.get_num_key(file)
        posts = self._load()

        posts[numKey] = {"localHash": localHash, "postId": postId}

        self._save(posts)
