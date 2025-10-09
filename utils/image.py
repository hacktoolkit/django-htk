# Python Standard Library Imports
import typing as T
from io import BytesIO

# Django Imports
from django.core.files import File

# Third Party (PyPI) Imports
import requests
from PIL import Image, UnidentifiedImageError


def get_image_from_url(image_url):
    if image_url:
        response = requests.get(image_url)
        if response:
            from six import BytesIO
            image = open_image(BytesIO(response.content))
        else:
            image = None
    else:
        image = None
    return image


def open_image(f):
    try:
        f.seek(0)
        image = Image.open(f)
    except IOError:
        image = None
    return image


def _detect_format_from_signature(header: bytes) -> T.Optional[str]:
    """Detect image format from file signature bytes."""
    result = None
    if header.startswith(b'\xff\xd8\xff'):
        result = 'JPEG'
    elif header.startswith(b'\x89PNG\r\n\x1a\n'):
        result = 'PNG'
    elif header.startswith(b'GIF87a') or header.startswith(b'GIF89a'):
        result = 'GIF'
    elif header.startswith(b'BM'):
        result = 'BMP'
    elif header.startswith(b'RIFF') and b'WEBP' in header[:12]:
        result = 'WEBP'
    elif header.startswith(b'\x00\x00\x01\x00'):
        result = 'ICO'
    elif header.startswith(b'ftypheic'):
        result = 'HEIC'
    return result


def detect_image_format(file: T.Union[File, BytesIO]) -> T.Optional[str]:
    """
    Detect the format of an image file using PIL and file signature fallback.

    This function provides a replacement for the deprecated imghdr module,
    supporting common image formats through both PIL detection and manual
    file signature checking.

    Args:
        file (Union[File, BytesIO]): A Django File object or an in-memory
        BytesIO object containing the image data.

    Returns:
        Optional[str]: The detected image format (e.g., 'JPEG', 'PNG', 'HEIC'),
        or None if the format couldn't be detected.
    """
    # If it's a File object, read it into BytesIO
    if hasattr(file, 'read'):
        file_content = BytesIO(file.read())
        if hasattr(file, 'seek'):
            file.seek(0)  # Reset file pointer
    else:
        file_content = file

    # Try to detect image format using PIL first
    detected_format = None
    try:
        with Image.open(file_content) as img:
            detected_format = img.format
    except UnidentifiedImageError:
        pass

    # Fallback: Check file signatures manually since imghdr is deprecated
    # in Python 3.13
    if not detected_format:
        file_content.seek(0)
        header = file_content.read(32)  # Read first 32 bytes for signature detection
        detected_format = _detect_format_from_signature(header)

    return detected_format
