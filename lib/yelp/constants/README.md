# Yelp API Constants

Configuration constants for Yelp API integration.

## Configuration Settings

```python
from htk.lib.yelp.constants import HTK_YELP_CLIENT_ID, HTK_YELP_API_KEY
```

## API Authentication

Configure Yelp API credentials in Django settings:

```python
# settings.py
HTK_YELP_CLIENT_ID = 'your-client-id'
HTK_YELP_API_KEY = 'your-api-key'
```

## Usage Example

```python
from htk.lib.yelp.constants import HTK_YELP_API_KEY

# Use the API key for authentication
headers = {
    'Authorization': f'Bearer {HTK_YELP_API_KEY}',
}
```
