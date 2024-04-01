# Python Standard Library Imports
import html
import re


# isort: off


def sanitize_cookie_value(value: str) -> str:
    """Sanitize Cookie Value

    Sanitizes a cookie value by escaping HTML special characters and
    removing non-alphanumeric characters, except for some safe ones like
    hyphens and underscores.

    Args:
    - value (str): The cookie value to be sanitized.

    Returns:
    - str: The sanitized cookie value.

    References:
    - https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/Set-Cookie
    - https://stackoverflow.com/a/1969339
    """
    # Escape HTML special characters to prevent XSS
    sanitized_value = html.escape(value)

    # Further restrict to a safe set of characters
    # This regular expression allows only alphanumeric characters, hyphens, and underscores
    sanitized_value = re.sub(r'[^a-zA-Z0-9-_]', '', sanitized_value)
    return sanitized_value
