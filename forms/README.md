# HTK Forms Module

> Django form utilities, custom fields, widgets, and model form helpers.

## Purpose

The forms module provides reusable Django form components and utilities to reduce boilerplate when building consistent forms. It includes abstract base classes, custom fields, widgets, and utilities for form validation and manipulation.

## Quick Start

```python
from django.db import models
from django import forms
from htk.forms.classes import AbstractModelInstanceUpdateForm

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(blank=True)
    location = models.CharField(max_length=100, blank=True)

class UserProfileForm(AbstractModelInstanceUpdateForm):
    class Meta:
        model = UserProfile
        fields = ['bio', 'location']

# Use in view
form = UserProfileForm(request.POST, instance=profile)
if form.is_valid():
    form.save()
```

## Key Components

| Component | Purpose |
|-----------|---------|
| **AbstractModelInstanceUpdateForm** | Base class for model instance update forms |
| **AbstractModelInstanceAttributesForm** | Base class for forms with dynamic attributes |
| **Custom Fields** | Email, URL, Date/Time fields with validation |
| **Custom Widgets** | Enhanced select, date picker, rich text widgets |
| **Form Utilities** | Error handling, attribute setting, field generation |

## Common Patterns

### Model Instance Update Form with Custom Fields

```python
from htk.forms.classes import AbstractModelInstanceUpdateForm
from htk.forms.fields import CustomEmailField

class ContactUpdateForm(AbstractModelInstanceUpdateForm):
    email = CustomEmailField(label="Email Address")

    class Meta:
        model = Contact
        fields = ['name', 'email', 'phone']

    def clean_phone(self):
        """Validate phone format"""
        phone = self.cleaned_data.get('phone')
        if phone and len(phone) < 10:
            raise forms.ValidationError("Phone must be at least 10 digits")
        return phone
```

### Form Validation with Cross-Field Checking

```python
class RegistrationForm(forms.Form):
    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput)
    password_confirm = forms.CharField(widget=forms.PasswordInput)

    def clean_email(self):
        """Check email not already registered"""
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("Email already registered")
        return email

    def clean(self):
        """Verify passwords match"""
        cleaned_data = super().clean()
        if cleaned_data.get('password') != cleaned_data.get('password_confirm'):
            raise forms.ValidationError("Passwords do not match")
        return cleaned_data
```

### Form with File Upload and Validation

```python
class DocumentUploadForm(AbstractModelInstanceUpdateForm):
    file = forms.FileField(label="Upload Document", help_text="Max 10MB")

    class Meta:
        model = Document
        fields = ['title', 'description', 'file']

    def clean_file(self):
        file = self.cleaned_data.get('file')
        if file and file.size > 10 * 1024 * 1024:
            raise forms.ValidationError("File exceeds 10MB limit")
        return file
```

### Custom Widget and Attribute Configuration

```python
from htk.forms.widgets import EnhancedSelect, DatePickerWidget
from htk.forms.utils import set_form_attributes

class ArticleForm(forms.Form):
    category = forms.ChoiceField(widget=EnhancedSelect(), choices=CATEGORIES)
    published_date = forms.DateField(widget=DatePickerWidget())

# Apply common styling
form = ArticleForm()
set_form_attributes(form, {
    'category': {'class': 'form-control'},
    'published_date': {'class': 'form-control'},
})
```

## Configuration

### Custom Placeholder Values

```python
# settings.py
HTK_FORMS_USE_CUSTOM_PLACEHOLDER_VALUES = True
HTK_FORMS_CUSTOM_PLACEHOLDER_VALUES = {
    'username': 'e.g. john_doe',
    'email': 'e.g. user@example.com',
    'password': 'e.g. securePassword123',
}
```

### Form Field Defaults

Available from `htk.forms.constants.defaults`:
- `FORM_DEFAULT_DISABLED = False`
- `FORM_DEFAULT_REQUIRED = True`
- `FORM_DEFAULT_INITIAL = {}`

## Best Practices

- **Inherit from abstract classes** - Reduces duplication, ensures consistency across forms
- **Validate at field level first** - Use `clean_<field>()` for single-field validation, then `clean()` for cross-field validation
- **Provide helpful error messages** - Be specific about what went wrong and how to fix it
- **Secure file uploads** - Validate size, type, and content; use CSRF protection
- **Use custom fields and widgets** - Apply consistent styling and validation across all forms

## Testing

```python
from django.test import TestCase
from myapp.forms import UserProfileForm

class FormTestCase(TestCase):
    def test_form_with_valid_data(self):
        form = UserProfileForm(data={'bio': 'My bio', 'location': 'NYC'})
        self.assertTrue(form.is_valid())

    def test_email_validation(self):
        form = UserProfileForm(data={'email': 'invalid-email'})
        self.assertFalse(form.is_valid())
        self.assertIn('email', form.errors)

    def test_file_size_validation(self):
        large_file = SimpleUploadedFile("file.pdf", b"x" * (11 * 1024 * 1024))
        form = DocumentUploadForm(files={'file': large_file})
        self.assertFalse(form.is_valid())
```

## Related Modules

- `htk.forms.classes` - Abstract form classes
- `htk.forms.fields` - Custom form fields
- `htk.forms.widgets` - Custom form widgets
- `htk.forms.utils` - Form utilities
- `htk.forms.constants` - Form configuration constants
- `htk.validators` - Validation functions

## References

- [Django Forms Documentation](https://docs.djangoproject.com/en/stable/topics/forms/)
- [Django Form Fields](https://docs.djangoproject.com/en/stable/ref/forms/fields/)
- [Django Form Widgets](https://docs.djangoproject.com/en/stable/ref/forms/widgets/)

## Notes

- **Status:** Production-Ready
- **Last Updated:** November 2025
- **Maintained by:** HTK Contributors
