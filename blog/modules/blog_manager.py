import markdown
import glob
import os

from .post_html_parser import PostHTMLParser
from .manager_base import ManagerBase
from .blog_metadata import BlogMetadata
from .blogger import Blogger
from .post_manager import PostManager
from .post_check_kind import PostCheckKind


class BlogManager(ManagerBase):
    def __init__(self, blogName="3930kmのいっぽめ", postGlobPattern="./posts/*.md") -> None:
        super().__init__()

        self._postHtmlParser = PostHTMLParser()
        self._blogger = Blogger()
        self._postManager = PostManager()
        self._blogName = blogName
        self._postGlobPattern = postGlobPattern

    def _get_post_files(self) -> list[str]:
        postGlobPattern = self._postGlobPattern
        files = glob.glob(postGlobPattern)
        return files

    def _convert_to_html(self, md_content: str) -> str:
        hash = self._calc_hash(md_content)
        html = markdown.markdown(md_content)
        result = """\
<!--
blog-meta-data
hash: {hash}
-->
""".format(hash=hash) + html
        return result

    def _get_metadata(self, html_content: str) -> BlogMetadata:
        _postHtmlParser = self._postHtmlParser
        _postHtmlParser.feed(html_content)
        return _postHtmlParser.get_blog_metadata()

    def _get_blog_id(self) -> str:
        blogger = self._blogger
        blogName = self._blogName
        blogs = [b for b in blogger.list_blogs() if b["name"] == blogName]
        if len(blogs) == 0:
            raise("'{blogName}' は存在しません".format(blogName=blogName))

        blog = blogs[0]

        blogId: str = blog["id"]
        return blogId

    def run(self):
        blogger = self._blogger
        postManager = self._postManager

        blogId: str = self._get_blog_id()

        files = self._get_post_files()
        for file in files:
            state = postManager.check(file)
            print("{file} : {state}".format(file=os.path.basename(
                file), state=str(state).split(".")[-1]))
            if state == PostCheckKind.NO_CHANGE:
                continue

            md_content = self._get_text_content(file)
            html_content = self._convert_to_html(md_content)
            metadata = self._get_metadata(html_content)

            title = metadata.title
            tags = metadata.tags

            if state == PostCheckKind.NEW:
                responsPost = blogger.insert(blogId=blogId, title=title,
                                             content=html_content, labels=tags)
                postId = responsPost["id"]
                postManager.update(file, metadata.hash, postId)
                print("\tINSERT SUCCESS")
            elif state == PostCheckKind.MODIFIED:
                postId = postManager.get_post_id(file)
                blogger.update(blogId=blogId, postId=postId, title=title,
                               content=html_content, labels=tags)

                postManager.update(file, metadata.hash, postId)
                print("\tUPDATE SUCCESS")
