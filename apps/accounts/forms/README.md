# Forms

## Classes
- **`UpdatePasswordForm`** (forms/auth.py) - A subclass of Django's SetPasswordForm
- **`PasswordResetFormHtmlEmail`** (forms/auth.py) - Modeled after django.contrib.auth.forms.PasswordResetForm
- **`UsernameEmailAuthenticationForm`** (forms/auth.py) - Based on django.contrib.auth.forms.AuthenticationForm

## Functions
- **`clean`** (forms/auth.py) - We are using cascaded_errors to bubble up any field-level errors to form-wide
- **`save`** (forms/auth.py) - Handles a possible race condition and performs save
- **`save`** (forms/auth.py) - Generates a one-use only link for resetting password and sends to the user
- **`clean`** (forms/auth.py) - Clean the form and try to get user
- **`clean`** (forms/auth.py) - We are using cascaded_errors to bubble up any field-level errors to form-wide
- **`has_username_field`** (forms/update.py) - Determines whether username is a field in this form instance
- **`clean_username`** (forms/update.py) - If username is a field in this form instance, ensure that it satisfies the regular expression
