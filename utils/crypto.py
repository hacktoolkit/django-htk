# Python Standard Library Imports
import base64
import hashlib
from six import string_types


# isort: off

class AESCipherCrypto:
    """Class for encrypting and decrypting data using AES256

    DEPRECATED: Only works in Python 2

    Source: https://stackoverflow.com/a/21928790/865091
    """
    def __init__(self, key=None):
        if not key:
            raise ValueError('``key`` is required for AESCipherCrypto')

        self.key = hashlib.sha256(key.encode('utf-8')).digest()

    def encrypt(self, raw):
        from Crypto import Random
        from Crypto.Cipher import AES

        raw = self._pad(raw)
        iv = Random.new().read(AES.block_size)
        cipher = AES.new(self.key, AES.MODE_CBC, iv)

        return base64.b64encode(iv + cipher.encrypt(raw.encode()))

    def decrypt(self, enc):
        from Crypto.Cipher import AES

        enc = base64.b64decode(enc)
        iv = enc[:AES.block_size]
        cipher = AES.new(self.key, AES.MODE_CBC, iv)

        return self._unpad(cipher.decrypt(enc[AES.block_size:])).decode('utf-8')

    def generate_key(self):
        raise NotImplementedError('``generate_key`` is not implemented in AESCipherCrypto')

    def _pad(self, s):
        from Crypto.Cipher import AES
        bs = AES.block_size
        return s + (bs - len(s) % bs) * chr(bs - len(s) % bs)

    @staticmethod
    def _unpad(s):
        return s[:-ord(s[len(s)-1:])]


class AESCipherFernet:
    """AES Cipher using ```cryptography.fernet.Fernet```

    Works both in Python 3 and Python 2.

    Python 2 produces some ``UserWarning``s.

    Docs: https://cryptography.io/en/latest/fernet/
    """
    def __init__(self, key=None):
        from cryptography.fernet import Fernet
        self._Fernet = Fernet

        self._key = key.encode('utf-8') if key else self._Fernet.generate_key()
        self._init_instance()

    def encrypt(self, content):
        content = self._process_content(content)

        value = self.instance.encrypt(content).decode('utf-8')

        return value

    def decrypt(self, content):
        content = self._process_content(content)

        value = self.instance.decrypt(content).decode('utf-8')

        return value

    def generate_key(self):
        self._key = self._Fernet.generate_key()
        self._init_instance()

        return self.key

    @property
    def key(self):
        value = self._key.decode('utf-8')

        return value

    def _process_content(self, content):
        if isinstance(content, string_types):
            content = content.encode('utf-8')

        return content

    def _init_instance(self):
        self.instance = self._Fernet(self._key)


class AESCipher(object):
    """Class for encrypting and decrypting data using AES256

    This class was originally using ``pycrypto`` PyPI package but it is no longer
    maintained and does not work with Python 3.x.

    If the project is using this, the data needs to be converted.

    Example converting:
    ```
    key = ...
    encrypted = ...

    old = AESCipher(key)
    new = AESCipher(key, use_fernet=True)
    data = new.encrypt(old.decrypt(encrypted))
    ```

    NOTE: If ``pycrypto`` package is not installed it will use Fernet by
    default and ``use_fernet`` init argument will not be effective.

    Python 3 Requirements:
     - cryptography
    Python 2 Requirements:
     - pycrypto
     - cryptography (optional)
    """

    def __init__(self, key=None, use_fernet=False):
        try:
            import Crypto  # noqa
        except ImportError:
            use_fernet = True

        klass = AESCipherFernet if use_fernet else AESCipherCrypto
        self.object = klass(key)

    def encrypt(self, content):
        value = self.object.encrypt(content)
        return value

    def decrypt(self, content):
        value = self.object.decrypt(content)
        return value

    def generate_key(self):
        value = self.object.generate_key()
        return value

    @property
    def key(self):
        value = self.object.key
        return value
