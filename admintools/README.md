# HTK Admintools Module

> Django admin extensions for user impersonation, role-based access control, and admin dashboard

## Purpose

The `admintools` module extends Django's admin functionality with company role management, user impersonation capabilities, and a comprehensive admin dashboard. It provides role-based access control (officers vs. employees), middleware for handling user emulation, permission decorators, and analytics views for migrations, TODOs, and system metrics.

## Directory Structure

```
admintools/
├── __init__.py                  # Module initialization
├── models.py                    # User role mixins (HtkCompanyUserMixin)
├── utils.py                     # Core utility functions (user roles, emulation)
├── views.py                     # Admin dashboard views (migrations, TODOs)
├── decorators.py                # Permission decorators (@company_officer_required)
├── middleware.py                # User emulation middleware (HtkEmulateUserMiddleware)
├── view_helpers.py              # Dashboard data collection (pulse metrics)
├── dataclasses.py               # Configuration data classes (TodosConfig)
├── cachekeys.py                 # Cache scheme definitions
└── constants/
    └── README.md                # [See constants/README.md](constants/README.md)
```

## Subdirectories

### [constants/](constants/README.md) - Admintools Constants
Admin tool configuration constants including company email domains, officer/employee email addresses, cookie expiration, pagination settings, and pulse dashboard limits.

## Key Components

### Models and Role Management

**HtkCompanyUserMixin** (models.py)
- `is_company_officer` - Cached property checking if user is company officer (staff/superuser or in officer emails list)
- `is_company_employee` - Cached property checking if user is company employee (in employee emails list)
- `has_company_email_domain` - Validates if user email matches company domain regex
- `should_display_htk_toolbar` - Determines HTK admin toolbar visibility
- `can_emulate_user` - Permission check for user impersonation

### User Emulation System

**Core Functions** (utils.py)
- `get_company_officers_id_email_map()` - Returns cached dict of officer IDs to emails
- `get_company_employees_id_email_map()` - Returns cached dict of employee IDs to emails
- `is_allowed_to_emulate_users(user)` - Checks if user has officer role
- `is_allowed_to_emulate(original_user, targeted_user)` - Validates emulation (prevents emulating officers)
- `request_emulate_user(request, user_id, username)` - Applies emulated user to request
- `emulate_user(request, ...)` - Sets emulation cookie and redirects

**Middleware** (middleware.py)
- `HtkEmulateUserMiddleware` - Processes cookies and applies emulated user to request
  - Reads `emulate_user_id` or `emulate_user_username` cookies
  - Applies emulation except in /admin and /admintools paths
  - Cleans up cookies on response

### Admin Dashboard Views

**views.py**
- `migrations_view()` - Displays list of all Django migrations from database
- `migration_plan_view()` - Shows pending/applied migrations and allows running migrations via subprocess
- `todos_view()` - Scans codebase for TODO comments organized by section

### Permission Decorators

**decorators.py**
- `@company_officer_required` - Restrict view access to company officers only
- `@company_employee_required` - Restrict view access to company employees only

### Analytics and Metrics

**view_helpers.py** - Pulse Dashboard Data Collection
- User registration trends (hourly, daily, weekly, monthly with averages)
- Login statistics (hourly, daily, weekly, monthly with averages)
- Recently joined users (configurable limit, default 50)
- Recent logins (configurable limit, default 50)
- Total user count

## Usage Examples

### Checking User Roles

```python
from django.contrib.auth.models import User

# Check if user is company officer
user = User.objects.get(pk=1)
if user.profile.is_company_officer:
    print("User has officer privileges")

# Check if user can emulate others
from htk.admintools.utils import is_allowed_to_emulate_users
if is_allowed_to_emulate_users(user):
    print("User can impersonate other users")
```

### Using Permission Decorators

```python
from django.shortcuts import render
from htk.admintools.decorators import company_officer_required

@company_officer_required
def admin_dashboard(request):
    """View restricted to company officers"""
    return render(request, 'admin/dashboard.html')

@company_officer_required
def manage_users(request):
    """Officer-only user management view"""
    users = User.objects.all()
    return render(request, 'admin/users.html', {'users': users})
```

### Emulating Users

```python
from htk.admintools.utils import emulate_user, is_allowed_to_emulate

# Check if emulation is allowed
target_user = User.objects.get(pk=5)
if is_allowed_to_emulate(request.user, target_user):
    # Emulate the user (sets cookie and redirects)
    return emulate_user(request, user_id=target_user.id)
```

### Accessing Pulse Dashboard Data

```python
from htk.admintools.view_helpers import get_pulse_data_users

pulse_data = get_pulse_data_users()
# Returns:
# {
#     'users': 1500,
#     'recently_joined_users': [...],
#     'registrations_last_month': 45,
#     'registrations_last_month_avg_hourly': '0.0644',
#     'logins_last_week': 300,
#     'logins_last_week_avg_hourly': '1.7857',
#     ...
# }
```

### Configuration

```python
# settings.py
HTK_COMPANY_EMAIL_DOMAINS = [
    r'.*@company\.com$',
    r'.*@internal\.company\.com$',
]

HTK_COMPANY_OFFICER_EMAILS = [
    'ceo@company.com',
    'admin@company.com',
    'ops@company.com',
]

HTK_COMPANY_EMPLOYEE_EMAILS = [
    'dev1@company.com',
    'dev2@company.com',
    'qa@company.com',
]

HTK_EMULATE_USER_COOKIE_EXPIRATION_MINUTES = 15

# Add middleware
MIDDLEWARE = [
    # ... other middleware ...
    'htk.admintools.middleware.HtkEmulateUserMiddleware',
]

# Add TODO scanning configuration
from htk.admintools.dataclasses import TodosConfig

HTK_ADMINTOOLS_TODOS_CONFIGS = [
    TodosConfig(
        name='Backend',
        directory='/path/to/backend',
        exclude_dirs=['migrations', '__pycache__', 'node_modules'],
        exclude_patterns=['*.pyc', '.git/*'],
    ),
]
```

## Access Control Patterns

### Pattern 1: Role-Based View Restrictions

```python
from django.core.exceptions import PermissionDenied
from django.contrib.auth.decorators import login_required

def officer_only_view(request):
    """Restrict view to officers"""
    if not (request.user.profile and request.user.profile.is_company_officer):
        raise PermissionDenied("Officer access required")
    # View logic here
    return render(request, 'officer_view.html')

# Or use decorator
from htk.admintools.decorators import company_officer_required

@company_officer_required
def officer_only_view_v2(request):
    """Same restriction with decorator"""
    return render(request, 'officer_view.html')
```

### Pattern 2: User Emulation in Admin Actions

```python
from htk.admintools.utils import emulate_user, is_allowed_to_emulate

def emulate_user_action(modeladmin, request, queryset):
    """Django admin action to emulate a user"""
    if queryset.count() != 1:
        modeladmin.message_user(request, "Select exactly one user")
        return

    target_user = queryset.first()
    if not is_allowed_to_emulate(request.user, target_user):
        modeladmin.message_user(request, "Cannot emulate this user")
        return

    return emulate_user(request, user_id=target_user.id)

# Register action
from django.contrib.auth.admin import UserAdmin
UserAdmin.actions.append(emulate_user_action)
```

### Pattern 3: Dashboard Analytics

```python
from django.shortcuts import render
from htk.admintools.view_helpers import get_pulse_data_users
from htk.admintools.decorators import company_officer_required

@company_officer_required
def system_pulse_view(request):
    """Show system metrics to officers"""
    pulse_data = get_pulse_data_users()
    context = {
        'total_users': pulse_data['users'],
        'recent_signups': pulse_data['recently_joined_users'],
        'registrations_trend': {
            'last_hour': pulse_data.get('registrations_last_hour', 0),
            'last_day': pulse_data.get('registrations_last_day', 0),
            'last_week': pulse_data.get('registrations_last_week', 0),
        },
        'login_trend': {
            'last_hour': pulse_data.get('logins_last_hour', 0),
            'last_day': pulse_data.get('logins_last_day', 0),
        },
    }
    return render(request, 'admin/pulse.html', context)
```

## Security Considerations

1. **Officer Emulation Prevention**: Officers cannot emulate other officers (prevents privilege escalation)
2. **Emulation Scope**: User emulation is disabled in `/admin` and `/admintools` paths
3. **Cookie Expiration**: Emulation cookies expire after configurable time (default 15 minutes)
4. **Role Caching**: Officer/employee status is cached with `@CachedAttribute` for performance
5. **Email-Based Roles**: Roles determined by email address membership (configurable in settings)

## Related Modules

- `htk.models` - User profile and base models
- `htk.cache` - Caching system with CustomCacheScheme
- `htk.constants` - Application-wide constants
- `htk.extensions.data_structures` - Cache data structures
- Django admin - Django's admin framework

## Best Practices

1. **Use Decorators for Permission Checks**
   - Always use `@company_officer_required` or `@company_employee_required` instead of manual checks
   - Provides consistent security and error handling

2. **Configure Role Settings Early**
   - Define `HTK_COMPANY_OFFICER_EMAILS` and `HTK_COMPANY_EMPLOYEE_EMAILS` in settings
   - Use email patterns for flexibility across environments

3. **Monitor Emulation Activity**
   - Log user emulation for audit trails
   - Set appropriate cookie expiration times (shorter = more secure)

4. **Test Role-Based Logic**
   - Ensure officers cannot emulate other officers
   - Verify emulation is disabled in admin areas
   - Test cookie cleanup on logout

## Testing

```python
from django.test import TestCase
from django.contrib.auth.models import User
from htk.admintools.utils import is_allowed_to_emulate

class AdmintoolsTestCase(TestCase):
    def setUp(self):
        self.officer = User.objects.create_user(
            username='officer',
            email='officer@company.com',
            is_staff=True,
            is_superuser=True,
        )
        self.user = User.objects.create_user(
            username='user',
            email='user@example.com',
        )

    def test_officer_can_emulate_user(self):
        """Officer should be able to emulate regular user"""
        self.assertTrue(is_allowed_to_emulate(self.officer, self.user))

    def test_officer_cannot_emulate_officer(self):
        """Officer should not be able to emulate another officer"""
        other_officer = User.objects.create_user(
            username='other_officer',
            email='other@company.com',
            is_staff=True,
            is_superuser=True,
        )
        self.assertFalse(is_allowed_to_emulate(self.officer, other_officer))

    def test_user_cannot_emulate(self):
        """Regular user should not be able to emulate anyone"""
        self.assertFalse(is_allowed_to_emulate(self.user, self.officer))
```

## References

- [Django User Authentication](https://docs.djangoproject.com/en/stable/topics/auth/)
- [Django Admin Site](https://docs.djangoproject.com/en/stable/ref/contrib/admin/)
- [Django Decorators](https://docs.djangoproject.com/en/stable/topics/http/decorators/)
- [Django Middleware](https://docs.djangoproject.com/en/stable/topics/http/middleware/)

## Notes

- Confidence: **HIGH** (>98%) - Clear architecture and patterns from code analysis
- Last Updated: November 2025
- Maintained by: HTK Contributors
