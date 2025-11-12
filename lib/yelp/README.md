# Yelp Integration

> Yelp API integration and utilities.

## Purpose

The yelp module provides integration with Yelp for seamless API communication and data synchronization.

## Quick Start

```python
from htk.lib.yelp import Client

# Initialize client with API credentials
client = Client(api_key='your_api_key')

# Make API calls
result = client.get_data()
```

## Configuration

```python
# settings.py
HTK_YELP_API_KEY = 'your_api_key'
HTK_YELP_ENABLED = True
```

## Common Patterns

### Authentication

```python
from htk.lib.yelp import Client

client = Client(api_key='key', api_secret='secret')
```

### Error Handling

```python
from htk.lib.yelp import Client, YelpError

try:
    result = client.api_call()
except YelpError as e:
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
from htk.lib.yelp import Client

class YelpTestCase(TestCase):
    def setUp(self):
        self.client = Client(api_key='test_key')

    @patch('htk.lib.yelp.requests.get')
    def test_api_call(self, mock_get):
        mock_get.return_value = Mock(status_code=200, json=lambda: {'data': 'test'})
        result = self.client.get_data()
        self.assertEqual(result['data'], 'test')
```

## Related Integrations

- Other `htk.lib.*` integrations

## References

- [Yelp API Documentation](https://www.yelp.com/docs/)
- HTK Integration Guide

## Notes

- **Status:** Production-Ready
- **Last Updated:** November 2025
- **Maintained by:** HTK Contributors
