# Egauge Integration

Energy monitoring and usage tracking.

## Quick Start

```python
from htk.lib.egauge import Client

client = Client(api_key='your_api_key')
result = client.get_data()
```

## Configuration

```python
# settings.py
EGAUGE_API_KEY = os.environ.get('EGAUGE_API_KEY')
```

## Related Modules

- `htk.lib.darksky` - Weather data
