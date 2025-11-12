# Shopify Integration

> Shopify API integration and utilities.

## Purpose

The shopify_lib module provides integration with Shopify for seamless API communication and data synchronization.

## Quick Start

```python
from htk.lib.shopify_lib import Client

# Initialize client with API credentials
client = Client(api_key='your_api_key')

# Make API calls
result = client.get_data()
```

## Configuration

```python
# settings.py
HTK_SHOPIFY_LIB_API_KEY = 'your_api_key'
HTK_SHOPIFY_LIB_ENABLED = True
```

## Common Patterns

### Authentication

```python
from htk.lib.shopify_lib import Client

client = Client(api_key='key', api_secret='secret')
```

### Error Handling

```python
from htk.lib.shopify_lib import Client, ShopifyError

try:
    result = client.api_call()
except ShopifyError as e:
    # Handle API errors
    pass
```

## Best Practices

- Use environment variables for API credentials
- Implement exponential backoff for retries
- Cache responses when appropriate
- Log API interactions for debugging
- Handle rate limiting gracefully

## Testing

```python
from django.test import TestCase
from unittest.mock import patch, Mock
from htk.lib.shopify_lib import Client

class ShopifyTestCase(TestCase):
    def setUp(self):
        self.client = Client(api_key='test_key')

    @patch('htk.lib.shopify_lib.requests.get')
    def test_api_call(self, mock_get):
        mock_get.return_value = Mock(status_code=200, json=lambda: {'data': 'test'})
        result = self.client.get_data()
        self.assertEqual(result['data'], 'test')
```

## Related Integrations

- Other `htk.lib.*` integrations

## References

- [Shopify API Documentation](https://www.shopify.com/docs/)
- HTK Integration Guide

## Notes

- **Status:** Production-Ready
- **Last Updated:** November 2025
- **Maintained by:** HTK Contributors
