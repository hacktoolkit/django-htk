# Literalword Integration

Bible content and scripture passages.

## Quick Start

```python
from htk.lib.literalword.utils import get_bible_passages

# Get bible passages
passages = get_bible_passages('John 3:16')
```

## Configuration

```python
# settings.py
LITERALWORD_API_KEY = os.environ.get('LITERALWORD_API_KEY')
```

## Related Modules

- `htk.apps.bible` - Scripture models
- `htk.lib.esv` - Bible translations
- `htk.lib.awesomebible` - Bible content
