# Form Utilities

Reusable base form classes and utilities for common validation patterns.

## Overview

The `forms` module provides:

- Abstract base form classes for common patterns
- Form utilities for field manipulation and error handling
- Integration with model forms
- Helper functions for form processing

## Base Form Classes

### AbstractModelInstanceUpdateForm

Base class for forms that update model instances:

```python
from htk.forms.classes import AbstractModelInstanceUpdateForm

class UserProfileForm(AbstractModelInstanceUpdateForm):
    class Meta:
        model = UserProfile
        fields = ['bio', 'website', 'location']
```

**Features:**
- Automatic model instance update
- Consistent error handling
- Field validation and cleaning

## Form Utilities

### Field Input Attributes

Set attributes on form input fields:

```python
from htk.forms.utils import set_input_attrs, set_input_placeholder_labels

# Set custom attributes
set_input_attrs(form, {'class': 'form-control', 'data-type': 'email'})

# Auto-populate placeholder with label
set_input_placeholder_labels(form)
```

### Error Handling

```python
from htk.forms.utils import get_form_errors, get_form_error

# Get all errors
all_errors = get_form_errors(form)  # List of all error messages

# Get first error
first_error = get_form_error(form)  # Single error string
```

### Model Instance Validation

```python
from htk.forms.utils import clean_model_instance_field

# Validate a field against model constraints
value = clean_model_instance_field(model_instance, field_name, value)
```

## Common Patterns

### Custom Form with Validation

```python
from django import forms
from htk.forms.classes import AbstractModelInstanceUpdateForm

class RegistrationForm(AbstractModelInstanceUpdateForm):
    password = forms.CharField(widget=forms.PasswordInput)
    password_confirm = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['username', 'email', 'password']

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        password_confirm = cleaned_data.get('password_confirm')

        if password != password_confirm:
            raise forms.ValidationError('Passwords do not match')

        return cleaned_data

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password'])
        if commit:
            user.save()
        return user
```

### API Form Handling

```python
from django.http import JsonResponse
from htk.api.utils import json_response_form_error

def api_update_user(request):
    form = UserUpdateForm(request.POST, instance=request.user)
    if form.is_valid():
        form.save()
        return JsonResponse({'success': True})
    else:
        return json_response_form_error(form)
```

### Dynamic Field Rendering

```python
from htk.forms.utils import set_input_attrs

def render_form(form, css_class='form-control'):
    set_input_attrs(form, {'class': css_class})
    set_input_placeholder_labels(form)
    return form
```

## Integration with Models

### Inherit from Abstract Models

```python
from htk.apps.accounts.models import BaseAbstractUserProfile

class CustomUserProfile(BaseAbstractUserProfile):
    department = models.CharField(max_length=100)

class UserProfileForm(AbstractModelInstanceUpdateForm):
    class Meta:
        model = CustomUserProfile
        fields = ['bio', 'website', 'department']
```

## Best Practices

1. **Extend AbstractModelInstanceUpdateForm** for model-related forms
2. **Use field validators** for single field validation
3. **Override clean()** for cross-field validation
4. **Set input attrs early** in form initialization
5. **Return JSON errors** in API views with `json_response_form_error`

## Classes

- **`AbstractModelInstanceUpdateForm`** - Base class for model update forms

## Functions

- **`save`** - Save form data to model instance
- **`clean_model_instance_field`** - Validate field against model
- **`set_input_attrs`** - Set HTML attributes on form fields
- **`set_input_placeholder_labels`** - Auto-populate field placeholders
- **`get_form_errors`** - Get all form errors as list
- **`get_form_error`** - Get first form error as string
