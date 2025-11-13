# Invitations App

User invitation and onboarding management.

## Overview

The `invitations` app provides:

- Create and send user invitations
- Track invitation lifecycle
- Email-based invitations with tokens
- Onboarding flow integration
- Invitation expiration and tracking

## Quick Start

### Send Invitations

```python
from htk.apps.invitations.models import BaseInvitation

# Create invitation
invitation = BaseInvitation.objects.create(
    email='user@example.com',
    invited_by=current_user,
    metadata={'team': 'engineering'}
)

# Send invitation email
invitation.send_email()
```

### Accept Invitations

```python
# User clicks link in email
@login_required
def accept_invitation(request, token):
    invitation = BaseInvitation.objects.get(token=token)

    # Connect user
    invitation.connect_user(request.user)

    # Complete invitation flow
    invitation.complete()

    return redirect('dashboard')
```

### Track Invitations

```python
# Get pending invitations
pending = BaseInvitation.objects.filter(accepted=False)

# Get invitations sent by user
my_invites = BaseInvitation.objects.filter(invited_by=user)

# Check invitation status
if invitation.is_expired:
    # Resend or delete
    pass
```

## Models

- **`BaseInvitation`** - Main invitation model

Extend to add custom data:

```python
from htk.apps.invitations.models import BaseInvitation

class CustomInvitation(BaseInvitation):
    department = CharField(max_length=100)
    role = CharField(max_length=100)
```

## Lifecycle

```
Create Invitation
    ↓
Send Email with Token
    ↓
User Clicks Link
    ↓
User Logs In / Signs Up
    ↓
Accept Invitation (connect to user)
    ↓
Complete Invitation
```

## Common Patterns

### Invitation with Role

```python
# Create invitation for specific role
invitation = BaseInvitation.objects.create(
    email='manager@company.com',
    invited_by=admin,
    metadata={'role': 'manager', 'org_id': 123}
)

# When accepted, use metadata
user = invitation.user
role = invitation.metadata.get('role')
org_id = invitation.metadata.get('org_id')
```

### Batch Invitations

```python
# Send multiple invitations
emails = ['user1@example.com', 'user2@example.com', 'user3@example.com']

for email in emails:
    invitation = BaseInvitation.objects.create(
        email=email,
        invited_by=organizer
    )
    invitation.send_email()
```

### Resend Invitations

```python
# Resend if not accepted
if not invitation.accepted:
    invitation.refresh_token()  # Get new token
    invitation.send_email()
```

## Configuration

```python
# settings.py
INVITATIONS_EXPIRY_DAYS = 7
INVITATIONS_EMAIL_TEMPLATE = 'emails/invitation.html'
INVITATIONS_FROM_EMAIL = 'noreply@example.com'
```

## Services

The app integrates with user creation:

```python
# Automatically called when user is created
process_user_created(user)

# Automatically called when email is confirmed
process_user_email_confirmation(user_email)

# Automatically called when user completes onboarding
process_user_completed(user)
```

## Best Practices

1. **Set clear expiration dates** on invitations
2. **Include context in metadata** (role, team, org)
3. **Send confirmation emails** after accept
4. **Track who invited whom** for analytics
5. **Allow resending** of expired invitations
6. **Validate email** before creating invitation
