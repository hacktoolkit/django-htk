# QR Code Helpers

Utilities for generating QR code images from text or URLs.

## Image generation

```python
from htk.lib.qrcode.utils import make_qr_code_image

png_image = make_qr_code_image('https://example.com')
svg_image = make_qr_code_image('https://example.com', image_format='svg')
```

Supported `image_format` values:

- `png` — default, returns a Pillow-backed image suitable for `image/png` responses.
- `svg` — returns a `qrcode.image.svg.SvgPathImage` suitable for `image/svg+xml` responses.

Unknown formats fall back to `png` for backwards compatibility.

## Django responses

```python
from htk.lib.qrcode.utils import qrcode_image_response

response = qrcode_image_response('https://example.com')
svg_response = qrcode_image_response('https://example.com', image_format='svg')
```

Restricted responses validate the generated key before serving the image:

```python
from htk.lib.qrcode.utils import generate_qr_key
from htk.lib.qrcode.utils import restricted_qrcode_image_response

url = 'https://example.com'
key = generate_qr_key(url)
response = restricted_qrcode_image_response(url, key=key, image_format='svg')
```

## Template tag

The `qrcode_image_url` tag accepts an optional format argument:

```django
{% load htk_tags %}
<img src="{% qrcode_image_url cpq_url 'svg' %}" alt="QR code" />
```

The endpoint still requires `HTK_QR_IMAGE_URL_NAME` and `HTK_QR_SECRET` settings for signed QR image URLs.
