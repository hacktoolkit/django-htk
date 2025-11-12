# Maintenance Mode App

> Application maintenance mode and downtime management.

## Purpose

The maintenance_mode app enables maintenance mode with custom messages and user whitelisting.

## Quick Start

```python
from htk.apps.maintenance_mode.models import *

# Create and use models
# See models.py for available classes
instance = YourModel.objects.create(field='value')
```

## Key Components

| Component | Purpose |
|-----------|---------|
| **Models** | MaintenanceMode configuration |
| **Views** | Provide web interface and API endpoints |
| **Forms** | Handle data validation and user input |
| **Serializers** | API serialization and deserialization |

## Common Patterns

### Basic Model Operations

```python
from htk.apps.maintenance_mode.models import *

# Create
obj = YourModel.objects.create(name='Example')

# Read
obj = YourModel.objects.get(id=1)

# Update
obj.name = 'Updated'
obj.save()

# Delete
obj.delete()
```

### Filtering and Querying

```python
# Filter by attributes
results = YourModel.objects.filter(status='active')

# Order by field
ordered = YourModel.objects.all().order_by('-created_at')

# Count results
count = YourModel.objects.filter(status='active').count()
```

## API Endpoints

| Endpoint | Method | Purpose |
|----------|--------|---------|
| `/api/maintenance_mode/` | GET | List items |
| `/api/maintenance_mode/` | POST | Create item |
| `/api/maintenance_mode/{id}/` | GET | Get item details |
| `/api/maintenance_mode/{id}/` | PATCH | Update item |
| `/api/maintenance_mode/{id}/` | DELETE | Delete item |

## Configuration

```python
# settings.py
HTK_MAINTENANCE_MODE_ENABLED = True
# Additional settings in constants/defaults.py
```

## Best Practices

- **Use ORM** - Leverage Django ORM for database queries
- **Validate input** - Use forms and serializers for validation
- **Check permissions** - Verify user has required permissions
- **Cache results** - Cache expensive queries and operations
- **Write tests** - Test models, views, forms, and API endpoints

## Testing

```python
from django.test import TestCase
from htk.apps.maintenance_mode.models import *

class Maintenance_ModeTestCase(TestCase):
    def setUp(self):
        """Create test fixtures"""
        self.obj = YourModel.objects.create(field='value')

    def test_model_creation(self):
        """Test creating an object"""
        self.assertIsNotNone(self.obj.id)
```

## Related Apps

- `htk.apps.accounts` - User accounts

## References

- [Django Models](https://docs.djangoproject.com/en/stable/topics/db/models/)
- [Django Forms](https://docs.djangoproject.com/en/stable/topics/forms/)

## Notes

- **Status:** Production-Ready
- **Last Updated:** November 2025
- **Maintained by:** HTK Contributors
