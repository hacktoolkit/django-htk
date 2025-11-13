# Template Tags

Django template filters and tags for common operations.

## Quick Start

```django
{% load htk_tags %}

<!-- Markdown conversion -->
{{ text|markdownify }}

<!-- Base64 encoding/decoding -->
{{ data|btoa }}
{{ encoded|atob }}

<!-- Phone formatting -->
{{ phone_number|phonenumber:"US" }}

<!-- QR codes -->
{% qrcode_image_url text as qr_url %}
<img src="{{ qr_url }}" alt="QR Code">
```

## Available Tags

### Text Processing

```django
<!-- Markdown to HTML -->
{{ markdown_text|markdownify }}

<!-- Obfuscate text (hide from bots) -->
{{ secret_text|obfuscate }}

<!-- Obfuscate email link -->
{{ email|obfuscate_mailto }}

<!-- Format phone number -->
{{ "2025551234"|phonenumber:"US" }}
```

### Encoding/Decoding

```django
<!-- Base64 encode -->
{{ text|btoa }}

<!-- Base64 decode -->
{{ encoded|atob }}
```

### Django Settings

```django
<!-- Get Django setting -->
{% get_django_setting "DEBUG" as debug_mode %}
{% if debug_mode %}
  <div>Debug mode enabled</div>
{% endif %}
```

### Asset Versions

```django
<!-- Include CSS with version -->
{% lesscss "main.css" %}

<!-- Include JS with version -->
{% loadjs "app.js" %}
```

### Template Rendering

```django
<!-- Render template string -->
{% render_string template_string with context_var=value %}
```

### Redirect Links

```django
<!-- Create redirect link -->
{% redir "example.com" %}

<!-- Create truncated redirect link -->
{% redir_trunc "https://example.com/very/long/url" max_length=30 %}
```

## Common Patterns

### Dynamic Content with Markdown

```django
<div class="content">
  {{ post.content|markdownify }}
</div>
```

### Email Obfuscation

```django
<!-- Prevent email harvesting -->
<p>Contact us: {{ "support@example.com"|obfuscate_mailto }}</p>
```

### QR Code Generation

```django
{% qrcode_image_url request.build_absolute_uri as qr_url %}
<img src="{{ qr_url }}" alt="Share this page">
```

### HTTP Header Formatting

```django
{% http_header "CONTENT_TYPE" %}
```

## Related Modules

- `htk.utils.text` - Text manipulation utilities
- `htk.lib.qrcode` - QR code generation
- `django.template` - Django template system
