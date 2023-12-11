# Python Standard Library Imports
import base64
import hashlib

# Third Party (PyPI) Imports
from Crypto import Random
from Crypto.Cipher import AES

# HTK Imports
from htk.compat import b64encode


# TODO: This needs to be refactored.
class AESCipher(object):
    """Class for encrypting and decrypting data using AES256

    Source: https://stackoverflow.com/a/21928790/865091
    """

    bs = AES.block_size

    def __init__(self, key):
        self.key = hashlib.sha256(key.encode()).digest()

    def encrypt(self, raw):
        raw = self._pad(raw)
        iv = Random.new().read(self.bs)
        cipher = AES.new(self.key, AES.MODE_CBC, iv)
        encoded = b64encode(iv + cipher.encrypt(raw.encode()))
        return encoded

    def decrypt(self, enc):
        # base64 encoded data is not convertible to `str` so not using `htk.compat.b64decode`
        enc = base64.b64decode(enc)
        iv = enc[:self.bs]
        cipher = AES.new(self.key, AES.MODE_CBC, iv)
        decrypted = self._unpad(cipher.decrypt(enc[self.bs:])).decode('utf-8')
        return decrypted

    @classmethod
    def _pad(cls, s):
        padded = s + (cls.bs - len(s) % cls.bs) * chr(cls.bs - len(s) % cls.bs)
        return padded

    @classmethod
    def _unpad(cls, s):
        unpadded = s[: -ord(s[len(s) - 1:])]
        return unpadded
