import base64
from abc import ABC, abstractmethod

from Cryptodome.Cipher import AES


class JobDataEncryptor(ABC):
    @abstractmethod
    def decrypt(self, content: str) -> str:
        pass

    @abstractmethod
    def encrypt(self, content: str) -> str:
        pass


class NoOpJobDataEncryptor(JobDataEncryptor):
    def decrypt(self, content: str) -> str:
        return content

    def encrypt(self, content: str) -> str:
        return content


class AESJobDataEncryptor:
    def __init__(self, secret_key: str):
        self.secret_key = base64.b64decode(secret_key)

    def decrypt(self, content: str) -> str:
        byte_array = base64.b64decode(content)
        context_bytes = byte_array[16:-16]
        cipher = AES.new(self.secret_key, AES.MODE_GCM, byte_array[:16])
        decrypted = cipher.decrypt_and_verify(context_bytes, byte_array[-16:])
        return decrypted.decode("UTF-8")

    def encrypt(self, content: str) -> str:
        byte_array = content.encode("UTF-8")
        cipher = AES.new(self.secret_key, AES.MODE_GCM)
        encrypted, tag = cipher.encrypt_and_digest(byte_array)
        return base64.b64encode(cipher.nonce + encrypted + tag).decode("UTF-8")
