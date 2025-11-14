# Forms Constants

## Overview

This module contains configuration values and constants used throughout the forms system, including widget styling mappings and input type definitions.

## Constants

### Widget Class Mappings

```python
from htk.forms.constants import HTK_FORM_WIDGET_CLASSES

# Maps form style names to widget-specific CSS classes
# Supports 'bootstrap' and 'pure' CSS frameworks
HTK_FORM_WIDGET_CLASSES = {
    'bootstrap': {
        'default': 'form-control',
        'TextInput': 'form-control',
        'Textarea': 'form-control',
        # ... other widget types
    },
    'pure': {
        'default': 'pure-input-1',
        'TextInput': 'pure-input-1',
        'Textarea': 'pure-input-1',
        # ... other widget types
    }
}
```

### Configuration Settings

```python
from htk.forms.constants import HTK_FORM_STYLE, HTK_DEFAULT_FORM_INPUT_CLASS

# Global form styling framework ('bootstrap' or 'pure')
HTK_FORM_STYLE = 'bootstrap'

# Default CSS class for form inputs (used when explicit class not specified)
HTK_DEFAULT_FORM_INPUT_CLASS = 'pure-input-1'
```

### Text Input Types

```python
from htk.forms.constants import TEXT_STYLE_INPUTS

# Tuple of Django form widget types that render as text-style inputs
TEXT_STYLE_INPUTS = ('EmailInput', 'NumberInput', 'PasswordInput', 'TextInput', 'Textarea', 'URLInput')
```

## Usage Examples

### Get CSS Class for Widget Type

```python
from htk.forms.constants import HTK_FORM_WIDGET_CLASSES, HTK_FORM_STYLE

style = HTK_FORM_STYLE
widget_type = 'TextInput'

css_class = HTK_FORM_WIDGET_CLASSES[style].get(widget_type, HTK_FORM_WIDGET_CLASSES[style]['default'])
# css_class = 'form-control' (if style is 'bootstrap')
```

### Check if Input Type is Text-Based

```python
from htk.forms.constants import TEXT_STYLE_INPUTS

widget_class_name = 'EmailInput'
is_text_input = widget_class_name in TEXT_STYLE_INPUTS
```

## Customization

Override these settings in `settings.py`:

```python
# Use Pure CSS instead of Bootstrap
HTK_FORM_STYLE = 'pure'

# Custom widget class mappings
HTK_FORM_WIDGET_CLASSES = {
    'custom': {
        'default': 'my-form-control',
        'TextInput': 'my-text-input',
    }
}
```
