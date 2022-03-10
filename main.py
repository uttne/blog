from copyreg import constructor
import markdown
import json
import glob
from html.parser import HTMLParser
import hashlib
import os
import pprint
import pickle

from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from enum import Enum


PP = pprint.PrettyPrinter(indent=2)


class BlogMetadata:
    def __init__(self, title: str = "", tags: list[str] = [], hash: str = "") -> None:
        self.title = title
        self.tags = tags
        self.hash = hash


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


class Blogger:
    def __init__(self, clientSecretFile="./client_secret.json", credentialCacheFile="./token.pickle") -> None:
        self._SCOPES = ['https://www.googleapis.com/auth/blogger']
        self._API_SERVICE_NAME = 'blogger'
        self._API_VERSION = 'v3'

        self._clientSecretFile = clientSecretFile
        self._credentialCacheFile = credentialCacheFile

        self._service = None

    def _get_credentials(self) -> Credentials:
        credentialCacheFile = self._credentialCacheFile
        clientSecretsFile = self._clientSecretFile
        scopes = self._SCOPES

        flow = InstalledAppFlow.from_client_secrets_file(
            clientSecretsFile, scopes)

        credentials = None
        if os.path.exists(credentialCacheFile):
            with open(credentialCacheFile, 'rb') as f:
                credentials = pickle.load(f)
        if not credentials or not credentials.valid:
            if credentials and credentials.expired and credentials.refresh_token:
                credentials.refresh(Request())
            else:
                credentials = flow.run_local_server(
                    host="localhost", port=28080, open_browser=True)
            with open(credentialCacheFile, 'wb') as f:
                pickle.dump(credentials, f)

        return credentials

    def _get_authenticated_service(self):
        apiServiceName = self._API_SERVICE_NAME
        apiVersion = self._API_VERSION
        credentials = self._get_credentials()

        service = self._service
        if(service):
            return service
        self._service = service = build(
            apiServiceName, apiVersion, credentials=credentials)
        return service

    def list_blogs(self):
        service = self._get_authenticated_service()
        result = service.blogs().listByUser(userId="self").execute()

        return result["items"]

    def insert(self, blogId: str, title: str, content: str, labels: list[str]):
        service = self._get_authenticated_service()
        posts = service.posts()

        body = {
            "title": title,
            "content": content,
            "labels": labels
        }
        response = posts.insert(
            blogId=blogId, isDraft=False, body=body).execute()

        return response

    def update(self, blogId: str, postId: str, title: str, content: str, labels: list[str]):
        service = self._get_authenticated_service()
        posts = service.posts()

        body = {
            "title": title,
            "content": content,
            "labels": labels
        }
        response = posts.update(
            blogId=blogId, postId=postId, body=body).execute()

        return response

    def list_posts(self, blogId: str):
        service = self._get_authenticated_service()
        posts = service.posts()

        response = posts.list(blogId=blogId).execute()

        return response["items"]


class PostCheckKind(Enum):
    NO_CHANGE = 0
    NEW = 1
    MODIFIED = 2


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

    def _getNumKey(self, file: str) -> str:
        fileName: str = os.path.basename(file)

        numStr = fileName.split("-", 1)[0]
        numKey = str(int(numStr))
        return numKey

    def check(self, file: str) -> PostCheckKind:

        numKey = self._getNumKey(file)

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

        numKey = self._getNumKey(file)

        posts = self._load()
        post = posts.get(numKey)
        return post["postId"]

    def update(self, file: str, localHash: str, postId: str) -> None:

        numKey = self._getNumKey(file)
        posts = self._load()

        posts[numKey] = {"localHash": localHash, "postId": postId}

        self._save(posts)


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


def main():
    bm = BlogManager()
    bm.run()


if __name__ == '__main__':
    main()
