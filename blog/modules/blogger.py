import os
import pickle

from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google.oauth2 import service_account

from .secret_manager import SecretManager


class Blogger:
    def __init__(
        self,
        clientSecretEncryptedFile="./client_secret.json.enc",
        credentialCacheFile="./token.pickle",
    ) -> None:
        self._SCOPES = ["https://www.googleapis.com/auth/blogger"]
        self._API_SERVICE_NAME = "blogger"
        self._API_VERSION = "v3"

        self._clientSecretEncryptedFile = clientSecretEncryptedFile
        self._credentialCacheFile = credentialCacheFile

        self._service = None

    def _get_credentials(self) -> Credentials:
        credentialCacheFile = self._credentialCacheFile
        clientSecretEncryptedFile = self._clientSecretEncryptedFile
        scopes = self._SCOPES

        sm = SecretManager()
        if not os.path.exists(clientSecretEncryptedFile):
            raise Exception(f"'{clientSecretEncryptedFile}' is not found.")

        passphrase = os.environ.get("BLOGGER_SECRET_ENCRYPT_PASSPHRASE")

        if not passphrase:
            raise Exception(f"'BLOGGER_SECRET_ENCRYPT_PASSPHRASE' is not found")

        with open(file=clientSecretEncryptedFile, mode="r", encoding="utf-8") as fp:
            encrypted_text = fp.read()
            config = sm.decrypt(encrypted_text, passphrase)

        flow = InstalledAppFlow.from_client_config(config, scopes)

        credentials = None
        if os.path.exists(credentialCacheFile):
            with open(credentialCacheFile, "rb") as f:
                credentials = pickle.load(f)
        if not credentials or not credentials.valid:
            if credentials and credentials.expired and credentials.refresh_token:
                credentials.refresh(Request())
            else:
                credentials = flow.run_local_server(
                    host="localhost", port=28080, open_browser=True, timeout_seconds=60
                )
            with open(credentialCacheFile, "wb") as f:
                pickle.dump(credentials, f)

        return credentials

    def _get_authenticated_service(self):
        apiServiceName = self._API_SERVICE_NAME
        apiVersion = self._API_VERSION
        credentials = self._get_credentials()

        service = self._service
        if service:
            return service
        self._service = service = build(
            apiServiceName, apiVersion, credentials=credentials
        )
        return service

    def list_blogs(self):
        service = self._get_authenticated_service()
        result = service.blogs().listByUser(userId="self").execute()

        return result["items"]

    def insert(self, blogId: str, title: str, content: str, labels: list[str]):
        service = self._get_authenticated_service()
        posts = service.posts()

        body = {"title": title, "content": content, "labels": labels}
        response = posts.insert(blogId=blogId, isDraft=False, body=body).execute()

        return response

    def update(
        self, blogId: str, postId: str, title: str, content: str, labels: list[str]
    ):
        service = self._get_authenticated_service()
        posts = service.posts()

        body = {"title": title, "content": content, "labels": labels}
        response = posts.update(blogId=blogId, postId=postId, body=body).execute()

        return response

    def list_posts(self, blogId: str):
        service = self._get_authenticated_service()
        posts = service.posts()

        response = posts.list(blogId=blogId).execute()

        return response["items"]
