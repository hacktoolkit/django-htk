# Awesomebible Integration

Bible content and scripture data.

## Quick Start

```python
from htk.lib.awesomebible import Client

client = Client(api_key='your_api_key')
result = client.get_data()
```

## Configuration

```python
# settings.py
AWESOMEBIBLE_API_KEY = os.environ.get('AWESOMEBIBLE_API_KEY')
```

## Related Modules

- `htk.apps.bible` - Scripture models
- `htk.lib.esv` - Bible translations
- `htk.lib.literalword` - Bible content
