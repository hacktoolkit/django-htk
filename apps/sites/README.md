# Sites App

Multi-site Django support wrapper for managing multiple website domains.

## Quick Start

```python
from django.contrib.sites.models import Site
from htk.apps.sites.utils import get_current_site, get_site_name, build_absolute_url

# Get current site
site = get_current_site(request)
domain = site.domain
name = site.name

# Build absolute URL
url = build_absolute_url(request, '/path/to/resource/')

# Use in templates
site_domain = request.site.domain
```

## Multi-Site Setup

### Configure Sites

```python
# settings.py
SITE_ID = 1

# Create multiple sites
from django.contrib.sites.models import Site

# Site 1
site1 = Site.objects.get_or_create(
    id=1,
    defaults={
        'domain': 'example.com',
        'name': 'Example'
    }
)

# Site 2 (different domain)
site2 = Site.objects.get_or_create(
    id=2,
    defaults={
        'domain': 'example.co.uk',
        'name': 'Example UK'
    }
)
```

### Get Current Site

```python
from django.contrib.sites.shortcuts import get_current_site
from htk.apps.sites.utils import get_current_site as htk_get_current_site

# Django built-in
site = get_current_site(request)

# HTK wrapper with fallback
site = htk_get_current_site(request)
```

## Common Patterns

### Build URLs

```python
from django.contrib.sites.shortcuts import get_current_site

def build_absolute_url(request, path):
    """Build absolute URL with domain"""
    site = get_current_site(request)
    protocol = 'https' if request.is_secure() else 'http'
    return f'{protocol}://{site.domain}{path}'

# Usage
reset_link = build_absolute_url(request, f'/auth/reset/{token}/')
```

### Site-Specific Settings

```python
from django.contrib.sites.shortcuts import get_current_site

class SiteConfig:
    CONFIGS = {
        'example.com': {
            'theme': 'default',
            'language': 'en',
            'timezone': 'US/Eastern'
        },
        'example.co.uk': {
            'theme': 'uk',
            'language': 'en-GB',
            'timezone': 'Europe/London'
        }
    }

    @classmethod
    def get_config(cls, domain):
        return cls.CONFIGS.get(domain, cls.CONFIGS['example.com'])

# Usage
def my_view(request):
    site = get_current_site(request)
    config = SiteConfig.get_config(site.domain)
    return render(request, 'view.html', {'config': config})
```

### Site-Specific Email Templates

```python
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string

def send_site_email(request, user, template_name, context):
    """Send email with site-specific template"""
    site = get_current_site(request)

    # Try site-specific template first
    try:
        html = render_to_string(
            f'emails/{site.domain}/{template_name}',
            context
        )
    except TemplateDoesNotExist:
        # Fall back to default
        html = render_to_string(
            f'emails/{template_name}',
            context
        )

    send_mail(
        subject=f'Message from {site.name}',
        message=html,
        from_email=f'noreply@{site.domain}',
        recipient_list=[user.email]
    )
```

### Site-Specific Content

```python
from django.contrib.sites.models import Site
from django.db import models

class Article(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    sites = models.ManyToManyField(Site)  # Multi-site support
    created = models.DateTimeField(auto_now_add=True)

def get_site_articles(site):
    """Get articles for specific site"""
    return Article.objects.filter(sites=site)
```

### Canonical URLs

```python
from django.contrib.sites.shortcuts import get_current_site

def get_canonical_url(request, path):
    """Get canonical URL for SEO"""
    site = get_current_site(request)
    protocol = 'https'
    return f'{protocol}://{site.domain}{path}'

# Usage in template
{% load sites %}
<link rel="canonical" href="{{ canonical_url }}" />
```

### Redirect to Site Domain

```python
from django.contrib.sites.shortcuts import get_current_site
from django.shortcuts import redirect

def enforce_site_domain(request):
    """Redirect if accessing from wrong domain"""
    site = get_current_site(request)

    if request.get_host() != site.domain:
        protocol = 'https' if request.is_secure() else 'http'
        url = f'{protocol}://{site.domain}{request.path}'
        return redirect(url, permanent=True)
```

## Template Usage

### In Templates

```django
{% load sites %}

<!-- Get current site -->
<footer>
    <p>&copy; {{ request.site.name }}</p>
    <a href="https://{{ request.site.domain }}/">Home</a>
</footer>

<!-- Link to site URL -->
<a href="https://{{ request.site.domain }}/about/">About Us</a>

<!-- Email footer -->
<p>Contact: support@{{ request.site.domain }}</p>
```

### Dynamic Base URL

```django
{% load sites %}

{% url 'home' as home_url %}
<a href="https://{{ request.site.domain }}{{ home_url }}">
    Go Home
</a>
```

## Configuration

```python
# settings.py
SITE_ID = 1  # Default site ID

# Enable sites framework
INSTALLED_APPS = [
    'django.contrib.sites',
    'htk.apps.sites',
    # ...
]

# Site-specific settings
SITE_DOMAINS = {
    1: 'example.com',
    2: 'example.co.uk',
    3: 'example.de',
}

SITE_THEMES = {
    'example.com': 'default',
    'example.co.uk': 'uk',
    'example.de': 'de',
}
```

## Best Practices

1. **Set SITE_ID in settings** - Configure default site
2. **Use get_current_site()** - Always get site dynamically
3. **Build absolute URLs** - Include protocol and domain
4. **Site-specific content** - Use through table for flexibility
5. **Canonical URLs** - Set for SEO with multiple domains
6. **Email templates** - Override per site
7. **Settings inheritance** - Provide defaults + overrides

## Related Modules

- `django.contrib.sites` - Django sites framework
- `htk.apps.accounts` - User management
- `htk.middleware` - Request processing
