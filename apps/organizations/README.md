# Organizations App

Multi-organization support with role-based access control and membership management.

## Overview

The `organizations` app provides:

- Create and manage organizations
- Role-based permissions (owner, manager, member)
- Organization invitations and member management
- Organization-specific settings
- Permission decorators for views

## Quick Start

### Create Organizations

```python
from htk.apps.organizations.models import BaseOrganization

# Create organization
org = BaseOrganization.objects.create(
    name='Acme Corporation',
    slug='acme-corp'
)

# Add members
org.add_member(user1, role='owner')
org.add_member(user2, role='manager')
org.add_member(user3, role='member')
```

### Invite Members

```python
from htk.apps.organizations.utils import invite_organization_member

# Send invitation
invite_organization_member(
    org=org,
    inviter=owner_user,
    email='newuser@example.com',
    role='member'
)

# User clicks link and accepts
# Automatically adds them to organization
```

### Manage Permissions

```python
# Check if user can manage org
if user in org.get_owners():
    # Show admin panel
    pass

# Get all members
members = org.get_members()

# Check specific permission
from htk.apps.organizations.decorators import require_organization_permission

@require_organization_permission('edit_members')
def edit_org_members(request, org_id):
    # Only org admins can access
    pass
```

## Models

- **`BaseOrganization`** - Main organization model
- **`BaseOrganizationMember`** - Tracks members and roles
- **`BaseOrganizationInvitation`** - Pending invitations

## Roles & Permissions

Default roles:
- **Owner** - Full access, manage members and settings
- **Manager** - Manage content, limited member access
- **Member** - Basic access to organization resources

Customize in your model:

```python
from htk.apps.organizations.models import BaseOrganization

class Organization(BaseOrganization):
    ROLE_CHOICES = (
        ('owner', 'Owner'),
        ('manager', 'Manager'),
        ('editor', 'Editor'),
        ('viewer', 'Viewer'),
    )

    role = CharField(choices=ROLE_CHOICES, default='member')
```

## Common Patterns

### Protect Views by Role

```python
from htk.apps.organizations.decorators import require_organization_permission

@require_organization_permission('manage_members')
def manage_org_members(request, org_id):
    org = BaseOrganization.objects.get(id=org_id)
    # Only users with permission can access
    return render(request, 'org/manage_members.html', {'org': org})
```

### Organization-Specific Data

```python
# Attach data to organizations
class Team(models.Model):
    organization = ForeignKey(BaseOrganization)
    name = CharField(max_length=100)
    members = ManyToManyField(User)

# Query org's teams
teams = org.team_set.all()
```

### Invitation Flow

```python
from htk.apps.organizations.models import BaseOrganizationInvitation

# Create invitation
invite = BaseOrganizationInvitation.objects.create(
    organization=org,
    invited_user_email='user@example.com',
    invited_by=request.user,
    role='member'
)

# Accept invitation
@login_required
def accept_invitation(request, token):
    invite = BaseOrganizationInvitation.objects.get(token=token)
    invite.accept()  # Adds user to org
    return redirect('org_dashboard')
```

### Bulk Operations

```python
# Get all users with specific role across orgs
from django.db.models import Q

admins = User.objects.filter(
    organizationmember__role='owner'
).distinct()

# Get orgs where user is owner
owned_orgs = BaseOrganization.objects.filter(
    members__user=user,
    members__role='owner'
)
```

## Settings & Configuration

```python
# settings.py
ORGANIZATIONS_INVITATION_EXPIRY = 7  # days
ORGANIZATIONS_REQUIRE_EMAIL_VERIFICATION = True
ORGANIZATIONS_DEFAULT_ROLE = 'member'
```

## Best Practices

1. **Extend BaseOrganization** for custom fields
2. **Use permission decorators** for access control
3. **Validate member additions** before saving
4. **Archive instead of delete** organizations
5. **Log organizational changes** for audit trail
6. **Cache membership** for performance

## Signals

Automatic signal handlers:
- `organization_invitation_created_or_updated` - Sends invitation email
