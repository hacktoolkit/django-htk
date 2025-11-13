# MongoDB Integration

NoSQL document database.

## Quick Start

```python
from htk.lib.mongodb import Client

client = Client(api_key='your_api_key')
result = client.get_data()
```

## Configuration

```python
# settings.py
MONGODB_URI = os.environ.get('MONGODB_URI')
MONGODB_DATABASE = os.environ.get('MONGODB_DATABASE')
```

## Related Modules

- `htk.apps.kv_storage` - Alternative data storage
