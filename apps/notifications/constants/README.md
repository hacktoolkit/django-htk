# Notifications Constants

## Overview

This module defines configuration for notification system behavior, including predicates for dismissible alerts and key generation strategies.

## Constants

### Alert Configuration

- **`HTK_NOTIFICATIONS_DISMISSIBLE_ALERT_DISPLAY_PREDICATES`** - Default: `{}` - Dict mapping alert types to display predicate functions
- **`HTK_NOTIFICATIONS_DISMISSIBLE_ALERT_KEY_GENERATORS`** - Default: `{}` - Dict mapping alert types to key generator functions

## Usage Examples

### Configure Alert Predicates

```python
# In Django settings.py
def should_show_upgrade_alert(request):
    return not request.user.is_premium

def should_show_verification_alert(request):
    return not request.user.email_verified

HTK_NOTIFICATIONS_DISMISSIBLE_ALERT_DISPLAY_PREDICATES = {
    'upgrade': should_show_upgrade_alert,
    'verify_email': should_show_verification_alert,
}
```

### Configure Alert Key Generators

```python
# In Django settings.py
def generate_upgrade_key(request):
    return f"upgrade_alert_{request.user.id}"

def generate_verification_key(request):
    return f"verify_alert_{request.user.id}"

HTK_NOTIFICATIONS_DISMISSIBLE_ALERT_KEY_GENERATORS = {
    'upgrade': generate_upgrade_key,
    'verify_email': generate_verification_key,
}
```
