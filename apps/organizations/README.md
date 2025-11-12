# Organizations App

> Organization/team management with hierarchical structure and role-based access control.

## Purpose

The organizations app provides organization and team management with hierarchical structures, role-based access control (RBAC), membership management, and organizational settings for multi-tenant applications.

## Quick Start

```python
from htk.apps.organizations.models import Organization, OrganizationMember

# Create organization
org = Organization.objects.create(
    name="Tech Company",
    slug="tech-company",
    owner=request.user,
    website="https://example.com"
)

# Add owner to organization
OrganizationMember.objects.create(
    organization=org,
    user=request.user,
    role='OWNER'
)

# Check member permissions
member = OrganizationMember.objects.get(organization=org, user=request.user)
if member.is_admin():
    # User can manage other members
    pass
```

## Key Components

| Component | Purpose |
|-----------|---------|
| **Organization** | Top-level company/organization entity |
| **OrganizationMember** | User membership with role (SYSADMIN, OWNER, ADMIN, MEMBER) |
| **OrganizationRole** | Custom role definitions with permissions |

## Role Hierarchy

```
SYSADMIN  → Full system access, can delete organization
OWNER     → Full organization control, can manage members
ADMIN     → Manage members and content
MEMBER    → Basic access, create/edit own content
```

## Common Patterns

### Organization Setup

```python
from htk.apps.organizations.models import Organization, OrganizationMember

# Create org with owner
org = Organization.objects.create(
    name="Company",
    slug="company",
    owner=user,
    description="Description",
    website="https://example.com"
)

# Add members with roles
OrganizationMember.objects.create(organization=org, user=admin_user, role='ADMIN')
OrganizationMember.objects.create(organization=org, user=member_user, role='MEMBER')
```

### Permission-Based Access

```python
def require_org_admin(view_func):
    """Decorator requiring organization admin role"""
    @wraps(view_func)
    def wrapped(request, org_id, *args, **kwargs):
        member = OrganizationMember.objects.get(
            organization_id=org_id,
            user=request.user
        )
        if not member.is_admin():
            raise PermissionDenied()
        return view_func(request, *args, **kwargs)
    return wrapped

@require_org_admin
def manage_members(request, org_id):
    # Only admins can access
    pass
```

### Bulk Member Operations

```python
# Add multiple members
members_data = [
    {'email': 'admin@example.com', 'role': 'ADMIN'},
    {'email': 'user@example.com', 'role': 'MEMBER'},
]

for data in members_data:
    user = User.objects.get(email=data['email'])
    OrganizationMember.objects.create(
        organization=org,
        user=user,
        role=data['role']
    )
```

## Configuration

```python
# settings.py
HTK_ORGANIZATION_REQUIRE_APPROVAL = False
HTK_ORGANIZATION_MAX_MEMBERS = None  # Unlimited
HTK_ORGANIZATION_ALLOW_CUSTOM_ROLES = True
HTK_ORGANIZATION_AUTO_ADD_OWNER_AS_ADMIN = True
```

## API Endpoints

| Endpoint | Method | Purpose |
|----------|--------|---------|
| `/api/organizations/` | GET | List user's organizations |
| `/api/organizations/` | POST | Create organization |
| `/api/organizations/{id}/members/` | GET | List members |
| `/api/organizations/{id}/members/` | POST | Add member |
| `/api/organizations/{id}/members/{user_id}/` | PATCH | Update member role |
| `/api/organizations/{id}/members/{user_id}/` | DELETE | Remove member |

## Best Practices

- **Least privilege** - Assign smallest necessary role; audit regularly
- **Always check permissions** - Use decorators for view protection
- **Implement approval workflows** - Support invitations before membership
- **Cache strategically** - Cache member counts and role checks
- **Audit extensively** - Log member changes, role updates, permission denials

## Testing

```python
from django.test import TestCase
from htk.apps.organizations.models import Organization, OrganizationMember

class OrganizationsTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='user1')
        self.org = Organization.objects.create(
            name='Test Org', slug='test-org', owner=self.user
        )

    def test_member_role_check(self):
        """Test member role verification"""
        member = OrganizationMember.objects.create(
            organization=self.org, user=self.user, role='ADMIN'
        )
        self.assertTrue(member.is_admin())
        self.assertFalse(member.is_owner())
```

## Related Apps

- `htk.apps.accounts` - User accounts
- `htk.apps.invitations` - Member invitations
- `htk.apps.notifications` - Organization notifications

## References

- [Role-Based Access Control](https://en.wikipedia.org/wiki/Role-based_access_control)
- [Django Permissions](https://docs.djangoproject.com/en/stable/topics/auth/)

## Notes

- **Status:** Production-Ready
- **Last Updated:** November 2025
- **Maintained by:** HTK Contributors
