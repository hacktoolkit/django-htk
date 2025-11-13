# ESV Integration

English Standard Version Bible API.

## Quick Start

```python
from htk.lib.esv import Client

client = Client(api_key='your_api_key')
result = client.get_data()
```

## Configuration

```python
# settings.py
ESV_API_KEY = os.environ.get('ESV_API_KEY')
```

## Related Modules

- `htk.apps.bible` - Scripture models
- `htk.lib.awesomebible` - Bible content
- `htk.lib.literalword` - Bible translations
