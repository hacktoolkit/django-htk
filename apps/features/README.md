# Features App

Feature flags for gradual rollouts, A/B testing, and feature management.

## Overview

The `features` app provides:

- Enable/disable features per user, organization, or globally
- Feature flag caching for performance
- A/B testing support
- Gradual feature rollout
- Feature metrics and tracking

## Quick Start

### Check Feature Flags

```python
from htk.apps.features.utils import get_feature_flag

# Check if feature is enabled for user
if get_feature_flag('new_dashboard', user):
    return render(request, 'new_dashboard.html')
else:
    return render(request, 'old_dashboard.html')

# Check global feature
if get_feature_flag('maintenance_mode'):
    return redirect('/maintenance/')
```

### Create Feature Flags

```python
from htk.apps.features.models import FeatureFlag

# Global flag
flag = FeatureFlag.objects.create(
    name='new_checkout',
    description='New checkout flow',
    is_active=True
)

# User-specific flag
flag.enable_for_user(user)
flag.disable_for_user(other_user)

# Percentage-based rollout
flag.set_percentage_rollout(10)  # 10% of users
```

### A/B Testing

```python
from htk.apps.features.utils import assign_variant

# Assign user to variant
variant = assign_variant('new_ui_test', user)

if variant == 'control':
    template = 'ui/control.html'
else:
    template = 'ui/new.html'

return render(request, template)
```

## Models

- **`FeatureFlag`** - Main feature flag model
- **`FeatureFlagUser`** - User-specific overrides
- **`FeatureFlagOrganization`** - Organization-specific settings

## Caching

Feature flags are automatically cached:

```python
from htk.apps.features.cachekeys import FeatureFlagCache

cache = FeatureFlagCache('feature_name')
cache.invalidate_cache()  # Refresh when flag changes
```

## Best Practices

1. **Use descriptive names** - `new_checkout_v2`, not `flag_1`
2. **Document purpose** - Add description when creating
3. **Monitor adoption** - Track which users have which features
4. **Gradual rollout** - Use percentage-based rollout before full launch
5. **Clean up old flags** - Remove completed experiments

## Typical Flow

1. Create flag (disabled by default)
2. Enable for internal testing
3. Enable for percentage of users
4. Monitor metrics
5. Roll out to 100% or disable
6. Remove flag code after full rollout

## Integration Examples

### In Templates

```django
{% if feature_flag 'new_dashboard' %}
  <!-- New dashboard content -->
{% else %}
  <!-- Legacy dashboard content -->
{% endif %}
```

### In Tests

```python
def test_new_feature(self):
    flag = FeatureFlag.objects.create(name='test_feature', is_active=True)
    flag.enable_for_user(self.user)

    response = self.client.get('/dashboard/')
    self.assertContains(response, 'New feature')
```

## Related Modules

- `htk.apps.accounts` - User management
- `htk.apps.organizations` - Org-level feature control
