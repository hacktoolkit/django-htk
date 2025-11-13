# HTK Validators Module

> Form and data validation utilities.

## Purpose

The validators module provides reusable validation functions for forms and data. These validators enforce data integrity and ensure values meet business logic requirements.

## Quick Start

```python
from htk.validators import is_valid_email, is_valid_url, is_valid_phone
from django import forms

class ContactForm(forms.Form):
    email = forms.EmailField(validators=[is_valid_email])
    website = forms.URLField(validators=[is_valid_url], required=False)
    phone = forms.CharField(validators=[is_valid_phone], required=False)

# Test validators
assert is_valid_email('user@example.com') == True
assert is_valid_email('invalid') == False
assert is_valid_url('https://example.com') == True
assert is_valid_phone('+1-555-0123') == True
```

## Key Components

| Function | Purpose |
|----------|---------|
| **is_valid_email()** | Validate email address format (RFC-compliant) |
| **is_valid_url()** | Validate URL format with scheme |
| **is_valid_phone()** | Validate phone number format |
| **Custom validators** | Build field-specific or cross-field validators |

## Common Patterns

### Field-Level Validation for Models and Forms

```python
from django.core.exceptions import ValidationError
from django.db import models

def validate_positive(value):
    """Validate value is positive"""
    if value <= 0:
        raise ValidationError("Value must be positive")

def validate_age(value):
    """Validate age is between 0 and 150"""
    if not (0 <= value <= 150):
        raise ValidationError("Age must be between 0 and 150")

# In model
class Person(models.Model):
    age = models.IntegerField(validators=[validate_age])
    quantity = models.IntegerField(validators=[validate_positive])

# In form
class PersonForm(forms.Form):
    age = forms.IntegerField(validators=[validate_age])
    quantity = forms.IntegerField(validators=[validate_positive])
```

### Cross-Field and Conditional Validation

```python
from django import forms
from django.core.exceptions import ValidationError

class RegistrationForm(forms.Form):
    email = forms.EmailField()
    email_confirm = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput)
    password_confirm = forms.CharField(widget=forms.PasswordInput)

    def clean(self):
        cleaned_data = super().clean()

        # Verify emails match
        if cleaned_data.get('email') != cleaned_data.get('email_confirm'):
            raise ValidationError("Emails do not match")

        # Verify passwords match
        if cleaned_data.get('password') != cleaned_data.get('password_confirm'):
            raise ValidationError("Passwords do not match")

        # Ensure email not already registered
        email = cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            self.add_error('email', "Email already registered")

        return cleaned_data
```

### Validator Classes for Complex Logic

```python
from django.core.exceptions import ValidationError

class PercentValidator:
    """Validate percentage value (0-100)"""
    def __call__(self, value):
        if not (0 <= value <= 100):
            raise ValidationError("Percentage must be between 0-100")

class SKUValidator:
    """Validate SKU format (3 letters + 6 digits)"""
    def __call__(self, value):
        import re
        if not re.match(r'^[A-Z]{3}[0-9]{6}$', value):
            raise ValidationError("SKU must be 3 letters followed by 6 digits")

# Use in models
class Product(models.Model):
    sku = models.CharField(max_length=20, validators=[SKUValidator()])
    discount = models.IntegerField(validators=[PercentValidator()])
```

## Best Practices

- **Use built-in validators first** - Django provides `MinValueValidator`, `MaxLengthValidator`, `RegexValidator`, etc.
- **Write clear error messages** - Be specific about what's invalid and what format is expected
- **Validate in order** - Combine field-level validators (format) then cross-field validators (relationships)
- **Test edge cases** - Valid inputs, boundary values, and invalid inputs
- **Separate concerns** - Keep validators simple; use form `clean()` for complex logic

## Testing

```python
from django.test import TestCase
from django.core.exceptions import ValidationError
from htk.validators import is_valid_email, is_valid_url, is_valid_phone

class ValidatorTestCase(TestCase):
    def test_email_validation(self):
        """Test email validation with valid and invalid inputs"""
        valid_emails = [
            'user@example.com',
            'user.name@example.co.uk',
            'user+tag@example.com',
        ]
        for email in valid_emails:
            self.assertTrue(is_valid_email(email))

        invalid_emails = ['invalid', 'user@', '@example.com', 'user @example.com']
        for email in invalid_emails:
            self.assertFalse(is_valid_email(email))

    def test_url_validation(self):
        """Test URL validation"""
        self.assertTrue(is_valid_url('https://example.com'))
        self.assertTrue(is_valid_url('http://sub.example.com/path'))
        self.assertFalse(is_valid_url('not a url'))
        self.assertFalse(is_valid_url('example.com'))  # Missing scheme

    def test_phone_validation(self):
        """Test phone validation"""
        self.assertTrue(is_valid_phone('5550123'))
        self.assertTrue(is_valid_phone('+1-555-0123'))
        self.assertFalse(is_valid_phone('123'))  # Too short
        self.assertFalse(is_valid_phone('abcdefgh'))  # Non-numeric
```
