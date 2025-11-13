# Decorators

Function and class decorators for common Django patterns.

## Overview

The `decorators` module provides:

- Function call deprecation warnings
- Signal handler control for testing
- View decorators for SEO and REST patterns
- Rate limiting for instance methods
- URL resolution helpers

## Function Deprecation

Mark functions as deprecated to warn users:

```python
from htk.decorators.classes import deprecated

@deprecated(version='2.0', alternative='new_function')
def old_function():
    pass

# Usage triggers deprecation warning
old_function()
# DeprecationWarning: old_function is deprecated (use new_function instead) [v2.0]
```

## Signal Handler Control

Disable signal handlers during testing or data loading:

```python
from htk.decorators.classes import disable_for_loaddata

@disable_for_loaddata
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)

# This handler won't fire during `python manage.py loaddata`
```

**Use Cases:**
- Prevent signal handlers from executing during fixture loading
- Test models without side effects
- Bulk import operations

## View Decorators

### SEO Redirect for RESTful Objects

Redirect to canonical SEO URL:

```python
from htk.decorators.classes import restful_obj_seo_redirect

@restful_obj_seo_redirect
def product_detail(request, product_id):
    product = Product.objects.get(id=product_id)
    if product.slug != request.resolver_match.kwargs.get('slug'):
        # Redirects to canonical URL with correct slug
        pass
```

### Resolve Records from REST URLs

Extract objects from URL patterns:

```python
from htk.decorators.classes import resolve_records_from_restful_url

@resolve_records_from_restful_url
def organization_detail(request):
    # Organization is automatically resolved from URL
    org = request.resolved_records['organization']
    return render(request, 'org_detail.html', {'org': org})
```

## Rate Limiting

### Rate Limit Instance Methods

Prevent method abuse with token bucket algorithm:

```python
from htk.decorators.rate_limiters import rate_limit_instance_method

class UserAPI:
    @rate_limit_instance_method(max_calls=10, period=60)
    def send_email(self, recipient, subject, body):
        # Allow max 10 calls per 60 seconds
        send_email_via_provider(recipient, subject, body)

# Usage
api = UserAPI()
for i in range(15):
    api.send_email('user@example.com', f'Message {i}', body)
    # Raises RateLimitError after 10 calls in 60 seconds
```

**Features:**
- Token bucket algorithm
- Per-instance rate limits
- Configurable time windows
- Automatic reset

## Common Patterns

### Deprecating Old Methods

```python
from htk.decorators.classes import deprecated

class UserService:
    @deprecated(version='2.0', alternative='create_user_v2')
    def create_user(self, email, password):
        return self.create_user_v2(email, password)

    def create_user_v2(self, email, password):
        # New implementation
        pass
```

### Safe Model Operations During Testing

```python
from django.db.models.signals import post_save
from htk.decorators.classes import disable_for_loaddata

@receiver(post_save, sender=User)
@disable_for_loaddata
def on_user_created(sender, instance, created, **kwargs):
    if created:
        # This won't run during loaddata/migrations
        send_welcome_email(instance.email)
```

### API Rate Limiting

```python
from htk.decorators.rate_limiters import rate_limit_instance_method

class StripePaymentGateway:
    @rate_limit_instance_method(max_calls=100, period=3600)
    def charge_card(self, card_token, amount):
        # Max 100 charges per hour
        return stripe.Charge.create(
            amount=amount,
            currency='usd',
            source=card_token
        )
```

## Classes

- **`restful_obj_seo_redirect`** - Redirect to canonical SEO URL for REST objects
- **`resolve_records_from_restful_url`** - Automatically resolve objects from URL kwargs
- **`rate_limit_instance_method`** - Rate limit instance method calls

## Functions

- **`deprecated`** - Mark function as deprecated with version info
- **`disable_for_loaddata`** - Disable signal handler during fixture loading

## Best Practices

1. **Use deprecation warnings** for API changes
2. **Disable signals in tests** with `disable_for_loaddata`
3. **Rate limit external API calls** to prevent abuse
4. **Provide alternatives** when deprecating
5. **Document rate limits** in docstrings

## Related Modules

- `django.utils.decorators` - Django's built-in decorators
- `functools` - Python's function decorators
- `htk.apps.accounts` - Auth decorators
- `htk.apps.organizations` - Permission decorators
