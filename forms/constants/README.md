# Forms Constants

> Django form styling and widget configuration for Bootstrap and PureCSS frameworks

## Purpose
This module provides constants for styling Django forms with CSS frameworks, defining input widget types, CSS class mappings, and default styling configurations for both Bootstrap and PureCSS.

## Key Files
- `__init__.py` - Exports text-style input widget types
- `defaults.py` - Default form style settings and widget-to-CSS-class mappings

## Key Components / Features

### Input Widget Types (`__init__.py`)
- `TEXT_STYLE_INPUTS` - Tuple of Django widget names that should receive text input styling:
  - EmailInput, NumberInput, PasswordInput, TextInput, Textarea, URLInput

### Form Styling Configuration (`defaults.py`)
- `HTK_FORM_STYLE` - Global form style setting (default: 'bootstrap', options: 'bootstrap', 'pure')
- `HTK_DEFAULT_FORM_INPUT_CLASS` - Default CSS class for form inputs (default: 'pure-input-1' for PureCSS)
- `HTK_FORM_WIDGET_CLASSES` - Comprehensive widget-to-CSS-class mapping dictionary

#### Widget Class Mappings
Supports both Bootstrap and PureCSS with mappings for:
- **Checkboxes**: CheckboxInput
- **Text Inputs**: EmailInput, NumberInput, PasswordInput, TextInput, Textarea, URLInput, DateInput, DateTimeInput, ClearableFileInput
- **Selects**: Select, SelectMultiple, NullBooleanSelect

Bootstrap classes use `form-control` and `form-check-input`, while PureCSS uses `pure-input-1` for all widgets.

## Usage

```python
from htk.forms.constants import TEXT_STYLE_INPUTS, HTK_FORM_STYLE
from htk.forms.constants.defaults import HTK_FORM_WIDGET_CLASSES

# Apply CSS classes to form widgets
class MyForm(forms.Form):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        widget_classes = HTK_FORM_WIDGET_CLASSES[HTK_FORM_STYLE]

        for field_name, field in self.fields.items():
            widget_name = field.widget.__class__.__name__
            css_class = widget_classes.get(widget_name, widget_classes['default'])
            field.widget.attrs['class'] = css_class

# Check if widget should have text styling
widget_type = 'EmailInput'
if widget_type in TEXT_STYLE_INPUTS:
    # Apply text-specific styling
    pass

# Switch form framework in settings
HTK_FORM_STYLE = 'bootstrap'  # or 'pure'
```

## Related Modules
- Parent: `htk/forms/`
- Related:
  - `htk.forms.utils` - Form utility functions using these constants
  - `htk.forms.widgets` - Custom widget implementations
  - `htk.forms.classes` - Form base classes with automatic styling

## Notes
- Confidence: HIGH (>98%)
- Last Updated: November 2025
- Supports Bootstrap (form-control) and PureCSS (pure-input-1) styling
- Can be overridden in Django settings to customize form styling globally
- Simplifies consistent form styling across entire application
