# Rabbitmq Integration

> Rabbitmq API integration and utilities.

## Purpose

The rabbitmq module provides integration with Rabbitmq for seamless API communication and data synchronization.

## Quick Start

```python
from htk.lib.rabbitmq import Client

# Initialize client with API credentials
client = Client(api_key='your_api_key')

# Make API calls
result = client.get_data()
```

## Configuration

```python
# settings.py
HTK_RABBITMQ_API_KEY = 'your_api_key'
HTK_RABBITMQ_ENABLED = True
```

## Common Patterns

### Authentication

```python
from htk.lib.rabbitmq import Client

client = Client(api_key='key', api_secret='secret')
```

### Error Handling

```python
from htk.lib.rabbitmq import Client, RabbitmqError

try:
    result = client.api_call()
except RabbitmqError as e:
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
from htk.lib.rabbitmq import Client

class RabbitmqTestCase(TestCase):
    def setUp(self):
        self.client = Client(api_key='test_key')

    @patch('htk.lib.rabbitmq.requests.get')
    def test_api_call(self, mock_get):
        mock_get.return_value = Mock(status_code=200, json=lambda: {'data': 'test'})
        result = self.client.get_data()
        self.assertEqual(result['data'], 'test')
```

## Related Integrations

- Other `htk.lib.*` integrations

## References

- [Rabbitmq API Documentation](https://www.rabbitmq.com/docs/)
- HTK Integration Guide

## Notes

- **Status:** Production-Ready
- **Last Updated:** November 2025
- **Maintained by:** HTK Contributors
