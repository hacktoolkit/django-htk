# Python Standard Library Imports
import base64
import sys


def is_python2():
    is_python2 = sys.version_info.major == 2
    return is_python2


def is_python3():
    is_python2 = sys.version_info.major == 3
    return is_python3


def has_min_python_version(major_version, minor_version):
    result = sys.version_info.major > major_version or (
        sys.version_info.major == major_version
        and sys.version_info.minor >= minor_version
    )
    return result


IS_PYTHON_2 = is_python2()
IS_PYTHON_3 = is_python3()


def b64encode(content, url_safe=False):
    """Base64 encoder with Python 2/3 compatibility

    Args:
        content: str | unicode (Python 2 only) | bytes (Python 3 only)
        url_safe: bool

    Returns: str
    """
    encoder = base64.urlsafe_b64encode if url_safe else base64.b64encode

    content = (
        content.encode()
        # Python 3 `base64.b64encode` requires the content to be `bytes`
        if (IS_PYTHON_3 and not isinstance(content, bytes))
        else content
    )
    encoded = encoder(content)

    # The result of Python 3 `base64.b64encode` is `bytes`, but we always want a `str`
    encoded = encoded.decode() if IS_PYTHON_3 else encoded

    return encoded


def b64decode(encoded, url_safe=False):
    """Base64 decoder with Python 2/3 compability

    Args:
        encoded: str | unicode | bytes
        url_safe: bool

    Returns: str
    """
    decoder = base64.urlsafe_b64decode if url_safe else base64.b64decode

    # `base64.b64decode` can decode either `str` or `bytes`, so no pre-treatment needed
    decoded = decoder(encoded)

    # The result of Python 3 `base64.b64decode` is `bytes`, but we always want a `str`
    decoded = decoded.decode() if IS_PYTHON_3 else decoded

    return decoded
