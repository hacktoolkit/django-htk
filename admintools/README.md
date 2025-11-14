# Admin Tools

Advanced admin functionality including user impersonation and company user management.

## Quick Start

```python
from htk.admintools.decorators import company_officer_required, company_employee_required
from htk.admintools.utils import is_allowed_to_emulate_users, request_emulate_user

# Protect views for company officers
@company_officer_required
def officer_dashboard(request):
    return render(request, 'officer_dashboard.html')

# Protect views for company employees
@company_employee_required
def employee_portal(request):
    return render(request, 'employee_portal.html')
```

## User Impersonation

Allow admins to emulate other users for testing:

```python
from htk.admintools.utils import is_allowed_to_emulate_users, request_emulate_user

# Check if user can emulate others
if is_allowed_to_emulate_users(request.user):
    # Allow user emulation in admin panel
    pass

# Emulate a specific user
request_emulate_user(request, original_user, target_user)
```

## Company User Management

Check company affiliation and roles:

```python
from htk.admintools.models import company_officer_required, is_company_officer, is_company_employee

# Check officer status
if is_company_officer(user):
    # User is a company officer
    pass

# Check employee status
if is_company_employee(user):
    # User is a company employee
    pass

# Check email domain
if user.has_company_email_domain():
    # User has company email
    pass
```

## Company Data Lookups

Get mappings of company users:

```python
from htk.admintools.utils import get_company_officers_id_email_map, get_company_employees_id_email_map

# Get officers mapping
officers = get_company_officers_id_email_map()
# Returns: {user_id: email, ...}

# Get employees mapping
employees = get_company_employees_id_email_map()
# Returns: {user_id: email, ...}
```

## Configuration

```python
# settings.py
# Enable company user features
COMPANY_ADMIN_ENABLED = True
```
