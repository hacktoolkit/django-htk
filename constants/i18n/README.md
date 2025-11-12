# I18N

> Constants for i18n.

## Purpose

The i18n constants define i18n configuration values.

## Quick Start

```python
from htk.constants.i18n import *

# Use utilities/constants
# See documentation for available exports
```

## Available Exports

| Name | Purpose |
|------|---------|
| See source code | Available functions and constants |

## Common Patterns

### Basic Usage

```python
from htk.constants.i18n import function_name, CONSTANT_NAME

# Use the functions and constants
result = function_name(param)
value = CONSTANT_NAME
```

## Configuration

Configuration handled in settings.py or module-level defaults.

## Best Practices

- Import only what you need
- Use constants instead of magic values
- Refer to source for complete documentation
- Follow module conventions

## Testing

```python
from django.test import TestCase
from htk.constants.i18n import *

class SubmoduleTestCase(TestCase):
    def test_functionality(self):
        # Add tests here
        pass
```

## Related Modules

- Parent module documentation
- Related utilities/constants

## References

- Source code documentation
- HTK Guidelines

## Notes

- **Status:** Production-Ready
- **Last Updated:** November 2025
- **Maintained by:** HTK Contributors
