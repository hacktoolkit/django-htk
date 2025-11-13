# Songselect Integration

Worship song and music library management.

## Quick Start

```python
from htk.lib.songselect import Client

client = Client(api_key='your_api_key')
result = client.get_data()
```

## Configuration

```python
# settings.py
SONGSELECT_API_KEY = os.environ.get('SONGSELECT_API_KEY')
```

## Related Modules

- `htk.lib.zesty` - Content management
