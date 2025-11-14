# Google Cloud Messaging (GCM) Utilities

Utilities for Google Cloud Messaging integration and push notification delivery.

## Functions

**get_gcm_client()**
- Initializes and returns a GCM (Google Cloud Messaging) client
- Reads API key from `HTK_GCM_API_KEY` setting
- Returns GCM instance if key is configured, None otherwise
- Uses the `gcm` library for message delivery

## Example Usage

```python
from htk.lib.google.cloud_messaging.utils import get_gcm_client

# Get GCM client
client = get_gcm_client()

if client:
    # Send message to device
    response = client.plaintext_request(
        registration_ids=['device_token_1', 'device_token_2'],
        data={'message': 'Hello World'}
    )
```

## Configuration

```python
# settings.py
HTK_GCM_API_KEY = 'your_gcm_api_key'
```

- `HTK_GCM_API_KEY` - Google Cloud Messaging API key for authentication
