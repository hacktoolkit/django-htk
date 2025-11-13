# Admintools

## Classes
- **`HtkCompanyOfficersCache`** (admintools/cachekeys.py) - Cache management object for company employees mapping
- **`HtkCompanyEmployeesCache`** (admintools/cachekeys.py) - Cache management object for company employees mapping
- **`TodosConfig`** (admintools/dataclasses.py) - Todos Config
- **`AdminToolsEntry`** (admintools/dataclasses.py) - Admin Tools Entry
- **`AdminToolsGroup`** (admintools/dataclasses.py) - Admin Tools Group
- **`HtkCompanyUserMixin`** (admintools/models.py) - Mixin for htk.apps.accounts.BaseAbstractUserProfile

## Functions
- **`company_officer_required`** (admintools/decorators.py) - Decorator for views that require access by company officer or staff user
- **`company_employee_required`** (admintools/decorators.py) - Decorator for views that require access by company employee or staff user
- **`process_request`** (admintools/middleware.py) - Replace the authenticated `request.user` if properly emulating
- **`process_response`** (admintools/middleware.py) - Delete user emulation cookies if they should not be set
- **`is_company_officer`** (admintools/models.py) - Determines whether this User is a company officer
- **`is_company_employee`** (admintools/models.py) - Determines whether this User is a company employee
- **`has_company_email_domain`** (admintools/models.py) - Determines whether this User has email with company domain
- **`get_company_officers_id_email_map`** (admintools/utils.py) - Gets a mapping of company officers
- **`get_company_employees_id_email_map`** (admintools/utils.py) - Gets a mapping of company employees
- **`is_allowed_to_emulate_users`** (admintools/utils.py) - Determines whether `user` is allowed to emulate other users
- **`is_allowed_to_emulate`** (admintools/utils.py) - Determines whether `original_user` is allowed to emulate `targeted_user`
- **`request_emulate_user`** (admintools/utils.py) - If all conditions are met, will modify the request to set an emulated user

## Components
**Views** (`views.py`)
