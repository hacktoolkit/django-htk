# Templatetags

## Functions
- **`markdownify`** (templatetags/htk_tags.py) - Converts Markdown string to HTML
- **`atob`** (templatetags/htk_tags.py) - Base64 decode
- **`btoa`** (templatetags/htk_tags.py) - Base64 encode
- **`phonenumber`** (templatetags/htk_tags.py) - Formats a phone number for a country
- **`obfuscate`** (templatetags/htk_tags.py) - Obfuscates a string
- **`obfuscate_mailto`** (templatetags/htk_tags.py) - Obfuscates a mailto link
- **`http_header`** (templatetags/htk_tags.py) - Converts Django HTTP headers to standard format
- **`get_django_setting`** (templatetags/htk_tags.py) - Retrieves a Django setting and sets it on the context dictionary
- **`render_string`** (templatetags/htk_tags.py) - Renders a Django template string with the given context
- **`lesscss`** (templatetags/htk_tags.py) - Determine whether to use LESS compilation on-the-fly or CSS files, and includes the appropriate one
- **`loadjs`** (templatetags/htk_tags.py) - Include a JS file and append a static asset version string
- **`qrcode_image_url`** (templatetags/htk_tags.py) - Returns the URL to the QR Code image of `qr_data`
- **`redir`** (templatetags/urlizer.py) - Links to a redirect page
- **`redir_trunc`** (templatetags/urlizer.py) - Links to a redirect page
