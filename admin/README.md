# HTK Admin Module

> Django admin customizations and abstract base classes for consistent admin interfaces.

## Purpose

The admin module provides reusable Django admin classes and decorators to reduce boilerplate when building consistent admin interfaces across multiple models.

## Quick Start

```python
from django.contrib import admin
from htk.admin.classes import AbstractAttributeAdmin
from myapp.models import Product

@admin.register(Product)
class ProductAdmin(AbstractAttributeAdmin):
    list_display = ['name', 'price', 'is_active']
    list_filter = ['is_active', 'created_at']
    search_fields = ['name', 'description']
    readonly_fields = ['created_at', 'updated_at']
```

## Key Components

| Component | Purpose |
|-----------|---------|
| **AbstractAttributeAdmin** | Base class for models with dynamic attributes |
| **admin decorators** | Performance and permission checking decorators |
| **custom admin site** | Custom AdminSite subclass for branding |

## Common Patterns

### Organized Fieldsets

```python
@admin.register(User)
class UserAdmin(AbstractAttributeAdmin):
    list_display = ['username', 'email', 'is_active']
    readonly_fields = ['created_at', 'updated_at']

    fieldsets = (
        ('Account', {'fields': ('username', 'email')}),
        ('Personal', {'fields': ('first_name', 'last_name')}),
        ('Permissions', {
            'fields': ('is_active', 'groups'),
            'classes': ('collapse',)
        }),
    )
```

### Custom List Display with Formatting

```python
from django.utils.html import format_html

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'colored_price', 'status_badge']

    def colored_price(self, obj):
        color = 'green' if obj.price < 100 else 'red'
        return format_html(
            '<span style="color: {};">${}</span>',
            color, obj.price
        )

    def status_badge(self, obj):
        return format_html(
            '<span style="color: {};">●</span> {}',
            'green' if obj.is_active else 'red',
            'Active' if obj.is_active else 'Inactive'
        )
```

### Inline Admin

```python
class BookInline(admin.TabularInline):
    model = Book
    extra = 1

@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    list_display = ['name', 'email']
    inlines = [BookInline]
```

### Permission-Based Fields

```python
@admin.register(SensitiveData)
class SensitiveDataAdmin(admin.ModelAdmin):
    def get_fields(self, request, obj=None):
        fields = ['name', 'description']
        if request.user.is_superuser:
            fields.append('api_key')
        return fields

    def get_readonly_fields(self, request, obj=None):
        if not request.user.is_superuser:
            return ['api_key']
        return []
```

## Best Practices

- **Organize fields with fieldsets** - Group related fields, use collapse for advanced options
- **Implement search** - Index searchable fields with `search_fields`
- **Use list filters** - Provide common filter options
- **Secure with permissions** - Check `has_change_permission()` and `has_delete_permission()`
- **Use raw_id_fields** - For large foreign key lists instead of dropdowns
- **Show key info in list_display** - Balance visibility with performance

## Testing

```python
from django.test import TestCase
from django.contrib.admin.sites import AdminSite
from myapp.models import Product
from myapp.admin import ProductAdmin

class ProductAdminTestCase(TestCase):
    def setUp(self):
        self.admin_site = AdminSite()
        self.admin = ProductAdmin(Product, self.admin_site)

    def test_list_display(self):
        """Verify list display fields."""
        self.assertEqual(
            self.admin.list_display,
            ['name', 'price', 'category']
        )
```

## Related Modules

- `htk.admintools` - Admin tools and utilities
- `django.contrib.admin` - Django admin framework
- `htk.decorators` - Function decorators

## References

- [Django Admin Documentation](https://docs.djangoproject.com/en/stable/ref/contrib/admin/)
- [Django Admin Actions](https://docs.djangoproject.com/en/stable/ref/contrib/admin/actions/)

## Notes

- **Status:** Production-Ready
- **Last Updated:** November 2025
- **Maintained by:** HTK Contributors
