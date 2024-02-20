# Third Party (PyPI) Imports
import requests
from PIL import Image


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
