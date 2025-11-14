# QR Code Constants

Configuration constants for QR code generation and validation.

## Configuration Settings

```python
from htk.lib.qrcode.constants import HTK_QR_SECRET
```

## QR Secret

Secret key used for signing/validating QR codes:

```python
# settings.py
HTK_QR_SECRET = 'your-secure-secret-key'
```

The default value should always be overridden in production:

```python
# Default (DO NOT USE IN PRODUCTION)
HTK_QR_SECRET = 'PLEASE_OVERRIDE_THIS_IN_DJANGO_SETTINGS'
```

## Usage Example

```python
from htk.lib.qrcode.constants import HTK_QR_SECRET

# Use the secret for signing QR code data
signature = generate_signature(data, HTK_QR_SECRET)
```
