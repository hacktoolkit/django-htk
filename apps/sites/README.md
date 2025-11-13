# Sites App

Multi-site Django support wrapper.

## Quick Start

```python
from django.contrib.sites.models import Site
from htk.apps.sites.utils import get_current_site, get_site_name

# Get current site
site = get_current_site(request)
domain = site.domain

# Get site name
name = get_site_name(request)
```

## Common Patterns

```python
# Create site
site = Site.objects.create(domain='example.com', name='Example')

# Build absolute URLs
from django.contrib.sites.shortcuts import get_current_site
site = get_current_site(request)
absolute_url = f'https://{site.domain}/path/'

# Use in templates
{{ request.site.domain }}
```

## Configuration

```python
# settings.py
SITE_ID = 1
```

## Related Modules

- `django.contrib.sites` - Official Django sites framework
