# QR Code Integration

QR code generation and image creation.

## Quick Start

```python
from htk.lib.qrcode.utils import qrcode_image_response, make_qr_code_image

# Generate QR code as HTTP response
response = qrcode_image_response('https://example.com')

# Generate QR code image
image = make_qr_code_image('https://example.com')
```

## Configuration

```python
# settings.py
QRCODE_ENABLED = True
```

## Related Modules

- `htk.lib.oembed` - Media embedding
