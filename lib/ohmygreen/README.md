# Ohmygreen Integration

Corporate wellness and meal benefits.

## Quick Start

```python
from htk.lib.ohmygreen import Client

client = Client(api_key='your_api_key')
result = client.get_data()
```

## Configuration

```python
# settings.py
OHMYGREEN_API_KEY = os.environ.get('OHMYGREEN_API_KEY')
```

## Related Modules

- `htk.lib.zesty` - Meal planning
