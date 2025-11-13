# RabbitMQ Integration

Message queue and asynchronous task processing.

## Quick Start

```python
from htk.lib.rabbitmq import Client

client = Client(api_key='your_api_key')
result = client.get_data()
```

## Configuration

```python
# settings.py
RABBITMQ_HOST = os.environ.get('RABBITMQ_HOST')
RABBITMQ_USER = os.environ.get('RABBITMQ_USER')
RABBITMQ_PASSWORD = os.environ.get('RABBITMQ_PASSWORD')
```

## Related Modules

- `htk.apps.async_task` - Async task queue
