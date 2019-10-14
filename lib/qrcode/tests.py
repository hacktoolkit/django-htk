from django.test import TestCase

class QrcodeLibTestCase(TestCase):
    def test_image_crop(self):
        import urllib
        from PIL import Image
        import StringIO
        file = StringIO.StringIO(urllib.urlopen('https://avatars2.githubusercontent.com/u/5404851?s=600&v=4').read())
        img = Image.open(file)
        img = img.crop((0, 0, 400, 600))
