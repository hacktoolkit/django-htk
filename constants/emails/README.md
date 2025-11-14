# Email Constants

## Overview

This module provides email validation constants, patterns for detecting invalid emails, and common email handles.

## Constants

### Bad Email Detection

```python
from htk.constants.emails import ALL_BAD_EMAILS, BAD_EMAIL_REGEXPS, LOCALHOST_EMAILS

# Set of email addresses known to be invalid or problematic
bad_emails = ALL_BAD_EMAILS  # includes 'root@localhost'

# Compiled regex patterns for detecting invalid email patterns
bad_patterns = BAD_EMAIL_REGEXPS

# Localhost email addresses that shouldn't be used
localhost = LOCALHOST_EMAILS  # {'root@localhost'}
```

### Common Email Handles

```python
from htk.constants.emails import COMMON_EMAIL_HANDLES

# Common generic email prefixes used by organizations
handles = COMMON_EMAIL_HANDLES
# ['company', 'contact', 'hello', 'hi', 'info', 'me', 'support', 'team', ...]
```

### Email Pattern Permutations

```python
from htk.constants.emails import EMAIL_PERMUTATION_PATTERNS

# 66 email pattern variations for generating possible email addresses
# Patterns use template variables like {first}, {last}, {domain}
patterns = EMAIL_PERMUTATION_PATTERNS
```

## Usage Examples

### Validate Email

```python
from htk.constants.emails import ALL_BAD_EMAILS

def is_valid_email(email):
    """Check if email is not in the bad emails list."""
    return email not in ALL_BAD_EMAILS
```

### Generate Email Permutations

```python
from htk.constants.emails import EMAIL_PERMUTATION_PATTERNS

def generate_emails(first_name, last_name, domain):
    """Generate possible email addresses using permutation patterns."""
    emails = []
    for pattern in EMAIL_PERMUTATION_PATTERNS:
        try:
            email = pattern.format(
                first=first_name.lower(),
                last=last_name.lower(),
                domain=domain.lower()
            )
            emails.append(email)
        except (KeyError, AttributeError):
            pass
    return emails
```
