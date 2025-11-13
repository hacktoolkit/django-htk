# Invitations Constants

## Overview

This module defines configuration for invitation systems, including model references and lifecycle signal settings.

## Constants

### Model References

- **`HTK_INVITATION_MODEL`** - Default: `None` - Primary invitation model (app_label.ModelName)
- **`HTK_INVITATION_MODELS`** - Default: `[]` - List of invitation models

### Lifecycle Configuration

- **`HTK_INVITATIONS_LIFECYCLE_SIGNALS_ENABLED`** - Default: `False` - Enable signal handlers for invitation lifecycle events

## Usage Examples

### Configure Invitation Models

```python
# In Django settings.py
HTK_INVITATION_MODEL = 'invitations.Invitation'
HTK_INVITATION_MODELS = [
    'invitations.Invitation',
    'organizations.OrganizationInvitation',
]
```

### Enable Lifecycle Signals

```python
# In Django settings.py
HTK_INVITATIONS_LIFECYCLE_SIGNALS_ENABLED = True
```

### Load and Use Models

```python
from django.apps import apps
from htk.apps.invitations.constants import HTK_INVITATION_MODEL

Invitation = apps.get_model(HTK_INVITATION_MODEL)
pending = Invitation.objects.filter(accepted=False)
```
