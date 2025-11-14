# Forms

## Overview

This forms module provides Django forms for handling user input, validation, and rendering form fields.

## Quick Start

### User Registration Form

```python
from htk.apps.accounts.forms.auth import UserRegistrationForm

def register_view(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            return redirect('login')
    else:
        form = UserRegistrationForm()

    return render(request, 'accounts/register.html', {'form': form})
```

### Change Password Form

```python
from htk.apps.accounts.forms.update import ChangePasswordForm

def change_password_view(request):
    if request.method == 'POST':
        form = ChangePasswordForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            return redirect('account_settings')
    else:
        form = ChangePasswordForm(request.user)

    return render(request, 'accounts/change_password.html', {'form': form})
```

### Form in Template

```django
<form method="post">
    {% csrf_token %}
    {{ form.as_p }}
    <button type="submit">Save Changes</button>
</form>
```

## Available Forms

Forms are defined in `forms.py` and provide:

- **Field validation** - Server-side validation of input
- **Widget customization** - HTML rendering and attributes
- **Error messages** - Clear error messages for invalid input
- **Help text** - Guidance for users on each field

## Validation

### Field Validation

Built-in validation for user registration:

```python
from htk.apps.accounts.forms.auth import UserRegistrationForm

# Validates:
# - username uniqueness
# - password strength
# - password confirmation match
# - email format (if email field present)
form = UserRegistrationForm(request.POST)
if form.is_valid():
    # All fields passed validation
    user = form.save()
```

### Custom Validation

```python
from htk.apps.accounts.forms.update import ChangeUsernameForm

class ChangeUsernameForm(UserUpdateForm):
    username = forms.CharField(max_length=30)

    def clean_username(self):
        username = self.cleaned_data['username']
        # Custom validation: check if username available
        if User.objects.filter(username=username).exists():
            raise forms.ValidationError('Username already taken')
        return username
```

## Form Usage

### Validate User Input

```python
from htk.apps.accounts.forms.auth import UserRegistrationForm

form = UserRegistrationForm(request.POST)
if form.is_valid():
    username = form.cleaned_data['username']
    user = form.save()
else:
    errors = form.errors  # Dict of all field errors
    username_errors = form.errors['username']  # Get specific field errors
```

### Create Form Instance

```python
from htk.apps.accounts.forms.update import UserUpdateForm

# Empty form
form = UserUpdateForm()

# With initial data
form = UserUpdateForm(initial={'email': 'user@example.com'})

# With POST data
form = UserUpdateForm(request.POST)

# With instance (update)
form = UserUpdateForm(instance=request.user)
```

## Best Practices

1. **Always validate** - Never trust user input
2. **Clear error messages** - Provide helpful validation feedback
3. **Use ModelForm** - For forms tied to Django models
4. **CSRF protection** - Always include {% csrf_token %}
5. **Test validation** - Test all validation rules
6. **Sanitize input** - Use Django built-in cleaning
7. **Help text** - Provide guidance for complex fields
