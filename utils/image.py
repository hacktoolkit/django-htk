import requests
from PIL import Image

def get_image_from_url(image_url):
    if image_url:
        response = requests.get(image_url)
        if response:
            import StringIO
            image = open_image(StringIO.StringIO(response.content))
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
