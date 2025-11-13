# DNS Constants

## Overview

This module defines DNS and domain-related constants including common top-level domains (TLDs).

## Constants

### Common TLDs

```python
from htk.constants.dns import COMMON_TLDS

# List of commonly-used top-level domains
common_tlds = COMMON_TLDS
# ['com', 'net', 'gov', ...]
```

## Usage

```python
from htk.constants.dns import COMMON_TLDS

def validate_tld(domain):
    """Check if domain uses a common TLD."""
    parts = domain.split('.')
    if parts:
        tld = parts[-1].lower()
        return tld in COMMON_TLDS
    return False
```
