# Zuora API Constants

Configuration constants and API endpoints for Zuora billing integration.

## Configuration Settings

```python
from htk.lib.zuora.constants import (
    HTK_ZUORA_CLIENT_ID,
    HTK_ZUORA_CLIENT_SECRET,
    HTK_ZUORA_COUNTRY,
    HTK_ZUORA_PROD,
    HTK_ZUORA_HANDLE_UNHANDLED_EVENTS,
    HTK_ZUORA_EVENT_TYPES,
    HTK_ZUORA_EVENT_HANDLERS,
    HTK_ZUORA_API_BASE_URLS,
)
```

## OAuth Configuration

```python
# settings.py
HTK_ZUORA_CLIENT_ID = 'your-client-id'
HTK_ZUORA_CLIENT_SECRET = 'your-client-secret'
HTK_ZUORA_COUNTRY = 'US'  # 'US' or 'EU'
HTK_ZUORA_PROD = True     # Use production environment
```

## API Base URLs

URLs for different regions and environments:

```python
HTK_ZUORA_API_BASE_URLS = {
    'US': {
        'prod': 'https://rest.zuora.com/',
        'sandbox': 'https://rest.apisandbox.zuora.com/',
    },
    'EU': {
        'prod': 'https://rest.eu.zuora.com/',
        'sandbox': 'https://rest.sandbox.eu.zuora.com/',
    },
}
```

## Event Handling

```python
# Event types
HTK_ZUORA_EVENT_TYPES = {
    'default': 'Default (unhandled) event',
    'subscription_created': 'Subscription created',
}

# Event handler mapping
HTK_ZUORA_EVENT_HANDLERS = {
    'default': 'htk.lib.zuora.event_handlers.default',
    'subscription_created': 'htk.lib.zuora.event_handlers.subscription_created',
}

# Handle unhandled events
HTK_ZUORA_HANDLE_UNHANDLED_EVENTS = False
```
