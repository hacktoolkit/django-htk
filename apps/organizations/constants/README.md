# Organizations Constants

## Overview

This module defines configuration for the organizations system, including model references, naming conventions, sorting preferences, and invitation settings.

## Constants

### Model References

- **`HTK_ORGANIZATION_MODEL`** - Default: `'organizations.Organization'`
- **`HTK_ORGANIZATION_ATTRIBUTE_MODEL`** - Default: `'organizations.OrganizationAttribute'`
- **`HTK_ORGANIZATION_MEMBER_MODEL`** - Default: `'organizations.OrganizationMember'`
- **`HTK_ORGANIZATION_INVITATION_MODEL`** - Default: `'organizations.OrganizationInvitation'`
- **`HTK_ORGANIZATION_JOIN_REQUEST_MODEL`** - Default: `'organizations.OrganizationJoinRequest'`
- **`HTK_ORGANIZATION_TEAM_MODEL`** - Default: `'organizations.OrganizationTeam'`
- **`HTK_ORGANIZATION_TEAM_MEMBER_MODEL`** - Default: `'organizations.OrganizationTeamMember'`
- **`HTK_ORGANIZATION_TEAM_POSITION_MODEL`** - Default: `'organizations.OrganizationTeamPosition'`
- **`HTK_ORGANIZATION_TEAM_MEMBER_POSITION_MODEL`** - Default: `'organizations.OrganizationTeamMemberPosition'`

### Display Configuration

- **`HTK_ORGANIZATION_READBLE_NAME`** - Default: `'Organization'` - Human-readable singular name
- **`HTK_ORGANIZATION_SYMBOL`** - Default: `'org'` - Short symbol for URLs/codes
- **`HTK_ORGANIZATION_URL_PK_KEY`** - Default: `'org_id'` - URL parameter name for organization ID

### Sorting Configuration

- **`HTK_ORGANIZATION_MEMBERS_SORT_ORDER`** - Default: `('user__first_name', 'user__last_name', 'user__username')`
- **`HTK_ORGANIZATION_TEAM_MEMBERS_SORT_ORDER`** - Default: `('user__first_name', 'user__last_name', 'user__username')`

### Invitation Configuration

- **`HTK_ORGANIZATION_INVITATION_RESPONSE_URL_NAME`** - Default: `''` - URL name for invitation response view
- **`HTK_ORGANIZATION_MOBILE_INVITATION_RESPONSE_URL_FORMAT`** - Default: `''` - Mobile invitation response URL format
- **`HTK_ORGANIZATION_INVITATION_EMAIL_TEMPLATE_NAME`** - Default: `''` - Email template for invitations
- **`HTK_ORGANIZATION_INVITATION_EMAIL_SUBJECT`** - Default: `'You have been invited to join {}'` - Email subject line

## Enums

### OrganizationMemberRoles

Roles for organization members with hierarchy:

```python
from htk.apps.organizations.enums import OrganizationMemberRoles

# Access role values
role = OrganizationMemberRoles.OWNER
print(f"{role.name}: {role.value}")  # OWNER: 1

# Available roles (hidden_choices excludes SYSADMIN)
OrganizationMemberRoles.SYSADMIN        # value: 0 (hidden)
OrganizationMemberRoles.OWNER           # value: 1
OrganizationMemberRoles.ADMIN           # value: 10
OrganizationMemberRoles.MEMBER          # value: 100

# Check if role is hidden
if role.is_hidden():
    print("This role is hidden from UI")
```

### OrganizationTeamMemberRoles

Roles for team members (subset of organization roles):

```python
from htk.apps.organizations.enums import OrganizationTeamMemberRoles

team_role = OrganizationTeamMemberRoles.ADMIN
OrganizationTeamMemberRoles.ADMIN       # value: 10
OrganizationTeamMemberRoles.MEMBER      # value: 100
```

## Usage Examples

### Configure Custom Models

```python
# In Django settings.py
HTK_ORGANIZATION_MODEL = 'myapp.Organization'
HTK_ORGANIZATION_TEAM_MODEL = 'myapp.Team'
HTK_ORGANIZATION_MEMBER_MODEL = 'myapp.Member'
```

### Load Models Dynamically

```python
from django.apps import apps
from htk.apps.organizations.constants import HTK_ORGANIZATION_MODEL

Organization = apps.get_model(HTK_ORGANIZATION_MODEL)
orgs = Organization.objects.all()
```

### Assign Member Roles

```python
from htk.apps.organizations.enums import OrganizationMemberRoles

# Assign a member role
member.role = OrganizationMemberRoles.ADMIN.value
member.save()

# Check role permissions
if member.role == OrganizationMemberRoles.OWNER.value:
    print("User can manage organization")
```

### Configure Invitations

```python
# In Django settings.py
HTK_ORGANIZATION_INVITATION_RESPONSE_URL_NAME = 'org_invite_response'
HTK_ORGANIZATION_INVITATION_EMAIL_TEMPLATE_NAME = 'emails/org_invitation.html'
HTK_ORGANIZATION_INVITATION_EMAIL_SUBJECT = 'You are invited to {}'
```
