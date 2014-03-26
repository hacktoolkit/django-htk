from django.test import TestCase

class QrcodeLibTestCase(TestCase):
    def test_image_crop(self):
        import urllib
        from PIL import Image
        import StringIO
        file = StringIO.StringIO(urllib.urlopen('https://fbstatic-a.akamaihd.net/rsrc.php/v2/yi/r/OBaVg52wtTZ.png').read())
        img = Image.open(file)
        img = img.crop((0, 0, 400, 600))
