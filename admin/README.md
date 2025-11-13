# Django Admin Utilities

Custom admin display and customization utilities.

## Quick Start

```python
from htk.admin.decorators import django_admin_bool_field

@django_admin_bool_field('is_active')
def is_active_display(obj):
    return obj.is_active
is_active_display.short_description = 'Active'

class UserAdmin(admin.ModelAdmin):
    list_display = ['username', is_active_display]
```

## Boolean Field Display

Display boolean fields as green checkmarks or red X marks in admin list view:

```python
from htk.admin.decorators import django_admin_bool_field

class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', is_available, is_featured]

    @django_admin_bool_field('is_available')
    def is_available(obj):
        return obj.is_available

    @django_admin_bool_field('is_featured')
    def is_featured(obj):
        return obj.is_featured
```

## Configuration

```python
# settings.py
ADMIN_SITE_HEADER = 'My Admin'
```
