import json
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from os import urandom
import base64


class SecretManager:
    def __init__(self):
        pass

    def encrypt(self, data: dict | list, passphrase: str) -> str:

        input_data = json.dumps(obj=data, ensure_ascii=False, indent=None)

        salt = urandom(16)
        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=32,
            salt=salt,
            iterations=100000,
            backend=default_backend(),
        )
        key = kdf.derive(passphrase.encode())

        iv = urandom(12)
        cipher = Cipher(algorithms.AES(key), modes.GCM(iv), backend=default_backend())
        encryptor = cipher.encryptor()

        encrypted_data = encryptor.update(input_data.encode()) + encryptor.finalize()

        base64_encoded = base64.b64encode(
            salt + iv + encryptor.tag + encrypted_data
        ).decode("utf-8")

        return base64_encoded

    def encrypt_file(
        self, input_file: str, passphrase: str, output_file: str | None = None
    ) -> None:

        with open(file=input_file, mode="r") as fp:
            encrypted_text = self.encrypt(data=json.load(fp=fp), passphrase=passphrase)

        output_file = output_file if output_file else input_file + ".enc"
        with open(file=output_file, mode="w") as fp:
            fp.write(encrypted_text)

    def decrypt(self, encrypted_text: str, passphrase: str) -> dict | list:

        combined_data = base64.b64decode(encrypted_text)
        salt = combined_data[:16]
        iv = combined_data[16:28]
        tag = combined_data[28:44]
        data = combined_data[44:]

        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=32,
            salt=salt,
            iterations=100000,
            backend=default_backend(),
        )
        key = kdf.derive(passphrase.encode())

        cipher = Cipher(
            algorithms.AES(key), modes.GCM(iv, tag), backend=default_backend()
        )
        decryptor = cipher.decryptor()

        decrypted_data = decryptor.update(data) + decryptor.finalize()

        decrypted_text = decrypted_data.decode()

        return json.loads(decrypted_text)

    def decrypt_file(
        self, input_file: str, passphrase: str, output_file: str | None = None
    ) -> None:

        with open(file=input_file, mode="r") as fp:
            decrypted_data = self.decrypt(
                encrypted_text=fp.read(), passphrase=passphrase
            )

        with open(file=output_file, mode="w") as fp:
            json.dump(
                fp=fp,
                obj=decrypted_data,
                ensure_ascii=False,
                indent=None,
                separators=(",", ":"),
            )
