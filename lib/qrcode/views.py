# Django Imports
from django.http import Http404


# isort: off


def qrcode_image(request):
    qr_key = request.GET.get('key', None)
    qr_data = request.GET.get('data', None)
    qr_format = request.GET.get('format', 'png')

    if qr_key and qr_data:
        from htk.lib.qrcode.utils import restricted_qrcode_image_response
        response = restricted_qrcode_image_response(
            data=qr_data,
            key=qr_key,
            image_format=qr_format,
        )
    else:
        response = None

    if response is None:
        raise Http404
    return response
