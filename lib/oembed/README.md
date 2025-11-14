# oEmbed Integration

Embed media content from URLs (YouTube, Vimeo, etc).

## Quick Start

```python
from htk.lib.oembed.utils import get_oembed_html, get_oembed_type

# Get embedding HTML for a URL
html = get_oembed_html('https://www.youtube.com/watch?v=dQw4w9WgXcQ')

# Get oEmbed type
embed_type = get_oembed_type('https://www.youtube.com/watch?v=dQw4w9WgXcQ')
# Returns: YouTube, Vimeo, etc

# Get HTML for specific service
vimeo_html = get_oembed_html_for_service('vimeo', 'https://vimeo.com/123456')
```

## Configuration

```python
# settings.py
OEMBED_ENABLED = True
```
