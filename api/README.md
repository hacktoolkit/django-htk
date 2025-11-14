# API Utilities

Tools for building REST APIs and handling common patterns.

## Overview

The `api` module provides utilities for:

- JSON responses with form errors
- Object retrieval with error handling
- Parameter extraction from requests
- DataTables server-side processing support

## Quick Reference

### Form Error Responses

Return form validation errors as JSON:

```python
from htk.api.utils import json_response_form_error

if not form.is_valid():
    return json_response_form_error(form)
```

### Safe Object Retrieval

Get an object or return a JSON error:

```python
from htk.api.utils import get_object_or_json_error

user = get_object_or_json_error(User, id=user_id)
if user:
    # object exists
else:
    # returns JSON error response
```

### Extract Parameters

Extract expected parameters from POST data:

```python
from htk.api.utils import extract_post_params

params = extract_post_params(request.POST, ['name', 'email', 'age'])
```

## DataTables Integration

Handle server-side DataTables requests with:

```python
from htk.api.views import model_datatables_api_get_view

# Add to your URL patterns
path('api/users/datatable/', model_datatables_api_get_view(User))
```

The view automatically handles:
- Sorting
- Filtering
- Pagination
- Column selection

## Classes

- **`DataTablesQueryParams`** - Parses DataTables query parameters from requests

## Functions

- **`json_response_form_error`** - Returns Django form errors as JSON response
- **`extract_post_params`** - Safely extracts expected parameters from POST data
- **`get_object_or_json_error`** - Retrieves object or returns JSON error
- **`model_datatables_api_get_view`** - Generic DataTables API view for any model
