# Invitations Constants

## Overview

This module defines configuration for invitation systems, including model references and lifecycle signal settings.

## Constants

### Model References

- **`HTK_INVITATION_MODEL`** - Default: `None` - Primary invitation model (app_label.ModelName)
- **`HTK_INVITATION_MODELS`** - Default: `[]` - List of invitation models

### Lifecycle Configuration

- **`HTK_INVITATIONS_LIFECYCLE_SIGNALS_ENABLED`** - Default: `False` - Enable signal handlers for invitation lifecycle events

## Enums

### InvitationStatus

Invitation lifecycle states:

```python
from htk.apps.invitations.enums import InvitationStatus

# Available invitation statuses with values
InvitationStatus.INITIAL           # value: 0 (Not yet sent)
InvitationStatus.EMAIL_SENT        # value: 1 (Email sent to recipient)
InvitationStatus.EMAIL_RESENT      # value: 2 (Email resent to recipient)
InvitationStatus.ACCEPTED          # value: 3 (Invitation accepted)
InvitationStatus.COMPLETED         # value: 4 (Fully completed)

# Access enum properties
status = InvitationStatus.EMAIL_SENT
print(f"{status.name}: {status.value}")  # EMAIL_SENT: 1

# Check invitation status
if status == InvitationStatus.ACCEPTED:
    print("Invitation was accepted")
```

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
