import qrcode

from PIL import Image

from django.http import HttpResponse

def qrcode_image_response(data=''):
    """Returns a QR Code image as an HTTP response

    TODO: Possible improvements: Cache (for a short period) requests for the same QR Code data-payload?
    """
    img = make_qr_code_image(data)
    #img = solid_color_image(width=200, height=200)

    response = HttpResponse(mimetype='image/png')
    img.save(response, 'png')
    return response

def make_qr_code_image(data='',
                       version=1,
                       error_correction=qrcode.constants.ERROR_CORRECT_M,
                       box_size=10,
                       border=4):
    """Generates a QR Code image

    Documentation: https://pypi.python.org/pypi/qrcode

    The `version` parameter is an integer from 1 to 40 that controls the size of the QR Code (the smallest, version 1, is a 21x21 matrix). Set to None and use the fit parameter when making the code to determine this automatically.

    The `error_correction` parameter controls the error correction used for the QR Code. The following four constants are made available on the qrcode package:

    ERROR_CORRECT_L
      About 7% or less errors can be corrected.
    ERROR_CORRECT_M (default)
      About 15% or less errors can be corrected.
    ERROR_CORRECT_Q
      About 25% or less errors can be corrected.
    ERROR_CORRECT_H.
      About 30% or less errors can be corrected.

    The `box_size` parameter controls how many pixels each "box" of the QR code is.

    The `border` parameter controls how many boxes thick the border should be (the default is 4, which is the minimum according to the specs).

    A shorthand with all of the defaults is possible:
    qrcode.make(data)
    """
    qr = qrcode.QRCode(
        version=version,
        error_correction=error_correction,
        box_size=box_size,
        border=border
    )
    qr.add_data(data)
    qr.make(fit=True)
    img = qr.make_image()
    return img

def solid_color_image(width=1, height=1, r=0, g=0, b=0, a=0):
    """
    TODO: Alpha channel is not working right now, for some reason; RGB channels work fine

    Documentation: http://pillow.readthedocs.org/en/latest/reference/Image.html
    """
    img = Image.new('RGBA', (width, height,), color=(r, g, b,))
#    img = Image.new('RGBA', (width, height,), color=(r, g, b,a,))
    return img
