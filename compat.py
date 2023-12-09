# Python Standard Library Imports
import base64

# Third Party (PyPI) Imports
from six import text_type


def b64encode(content, url_safe=False):
    """Base64 encoder with Python 2/3 compatibility

    Args:
        content: str | unicode | bytes
        url_safe: bool

    Return: str
    """
    encoder = base64.urlsafe_b64encode if url_safe else base64.b64encode

    content = content.encode()
    encoded = encoder(content)
    encoded = encoded.decode() if isinstance(encoded, bytes) else encoded

    return encoded


def b64decode(content, url_safe=False):
    """Base64 decoder with Python 2/3 compability

    Args:
        content: str | unicode | bytes
        url_safe: bool

    Return: str
    """
    decoder = base64.urlsafe_b64decode if url_safe else base64.b64decode

    content = content.encode() if isinstance(content, text_type) else content
    decoded = decoder(content)
    decoded = decoded.decode() if isinstance(decoded, bytes) else decoded

    return decoded
