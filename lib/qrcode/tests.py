# Django Imports
from django.test import TestCase
from django.test import override_settings

# HTK Imports
from htk.lib.qrcode.utils import generate_qr_key
from htk.lib.qrcode.utils import make_qr_code_image
from htk.lib.qrcode.utils import qrcode_image_response
from htk.lib.qrcode.utils import restricted_qrcode_image_response


class QrcodeLibTestCase(TestCase):
    def test_make_qr_code_image_supports_svg(self):
        img = make_qr_code_image('https://awesome.bible', image_format='svg')

        self.assertEqual(img.kind, 'SVG')

    def test_qrcode_image_response_supports_png_by_default(self):
        response = qrcode_image_response('https://awesome.bible')

        self.assertEqual(response['Content-Type'], 'image/png')
        self.assertTrue(response.content.startswith(b'\x89PNG\r\n\x1a\n'))

    def test_qrcode_image_response_supports_svg(self):
        response = qrcode_image_response('https://awesome.bible', image_format='svg')

        self.assertEqual(response['Content-Type'], 'image/svg+xml')
        self.assertIn(b'<svg', response.content)
        self.assertIn(b'</svg>', response.content)

    @override_settings(HTK_QR_SECRET='test-secret')
    def test_restricted_qrcode_image_response_supports_svg(self):
        data = 'https://awesome.bible'
        key = generate_qr_key(data)

        response = restricted_qrcode_image_response(
            data=data,
            key=key,
            image_format='svg',
        )

        self.assertEqual(response['Content-Type'], 'image/svg+xml')
        self.assertIn(b'<svg', response.content)

    def test_image_crop(self):
        import six.moves.urllib as urllib
        from PIL import Image
        import StringIO
        file = StringIO.StringIO(urllib.urlopen('https://avatars2.githubusercontent.com/u/5404851?s=600&v=4').read())
        img = Image.open(file)
        img = img.crop((0, 0, 400, 600))
