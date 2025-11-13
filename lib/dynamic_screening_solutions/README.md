# Dynamic_Screening_Solutions

## Classes
- **`Htk321FormsAPI`** (dynamic_screening_solutions/api.py) - 321Forms - Dynamic Screening Solutions

## Functions
- **`make_request_headers`** (dynamic_screening_solutions/api.py) - Creates a header to pass in for GET/POST request
- **`get_users_by_company`** (dynamic_screening_solutions/api.py) - Returns a list of users in a company based on `user_type` provided.
- **`get_onboarded_employee_users_by_company`** (dynamic_screening_solutions/api.py) - Returns a list of 100% onboarded users in the provided company.
- **`get_companies`** (dynamic_screening_solutions/api.py) - Returns a JSON response of companies that the user can access
- **`get_divisions_by_company`** (dynamic_screening_solutions/api.py) - Returns a JSON response with two elements. The companyID provided and an array of divisions
- **`get_forms_by_company`** (dynamic_screening_solutions/api.py) - Returns an array of the company's forms.
- **`get_form_by_company`** (dynamic_screening_solutions/api.py) - Returns an array of form questions and an object with the basic details of the form itself
- **`get_form_by_user`** (dynamic_screening_solutions/api.py) - Receives response information of a user's latest form of a particular status
- **`get_responses_by_user`** (dynamic_screening_solutions/api.py) - Receives response information to questions asked of a user
- **`validate_webhook_request`** (dynamic_screening_solutions/utils.py) - Validates a 321Forms webhook request

## Components
**Views** (`views.py`)
