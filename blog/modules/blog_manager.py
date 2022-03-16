import markdown
from markdown.extensions.codehilite import CodeHiliteExtension
from markdown.extensions.fenced_code import FencedCodeExtension
from git import Git
import glob
import os
import re
import pathlib

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

    def _convert_to_html(self, md_content: str, hash: str) -> str:
        html = markdown.Markdown(
            extensions=[FencedCodeExtension(), CodeHiliteExtension()]).convert(md_content)
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

    def _convert_image_url(self, file: str, md_content: str) -> str:
        dirName = os.path.dirname(file)
        g = Git(dirName)

        try:
            gitTopLevelDir: str = g.rev_parse("--show-toplevel")
            remoteUrl: str = g.config("--get", "remote.origin.url")
        except:
            raise("'dirName' は git レポジトリではありません")

        baseRemoteUrl = ""
        isGitHub = False
        urlMatch = re.search(r'https://(.+?)/', remoteUrl)
        if urlMatch:
            host = urlMatch.group(1)
            if host == "github.com":
                isGitHub = True
                # 後ろに / はつかない
                baseRemoteUrl = remoteUrl.rsplit(".", 1)[0].replace(
                    "github.com", "raw.githubusercontent.com")

        newContent = ""
        index = 0
        matchs = re.finditer(r'!\[.*?\]\((.+?)\)', md_content)
        for m in matchs:
            urlSpan = m.span(1)
            imageUrl: str = m.group(1)

            newContent += md_content[index:urlSpan[0]]

            newUrl = ""
            if isGitHub and imageUrl.startswith("."):
                filePath = imageUrl
                absFilePath = os.path.abspath(os.path.join(dirName, filePath))
                commitHash = g.log("-1", "--pretty=%H", "--", filePath)
                if(not commitHash):
                    raise("'{}' はコミットされていません".format(absFilePath))

                p = pathlib.Path(absFilePath)
                # 頭に / はつかない画像の相対パスを取得する
                relativePath = str(p.relative_to(
                    gitTopLevelDir)).replace("\\", "/")

                newUrl = baseRemoteUrl + "/" + commitHash + "/" + relativePath
            else:
                newUrl = imageUrl

            newContent += newUrl

            index = urlSpan[1]

        newContent += md_content[index:]

        return newContent

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

            # 読み込んだ Markdown の生のテキストのハッシュを計算する
            md_content = self._get_text_content(file)
            hash = self._calc_hash(md_content)

            new_md_content = self._convert_image_url(file, md_content)
            html_content = self._convert_to_html(new_md_content, hash)
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
