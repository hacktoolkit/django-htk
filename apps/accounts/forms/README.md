# Forms

Django forms for user input validation and rendering.

## Overview

This module provides Django forms for handling user input, validation, and rendering form fields.

## Quick Start

### Use Form in View

```python
from htk.apps.accounts.forms.forms import ItemForm

def create_item_view(request):
    if request.method == 'POST':
        form = ItemForm(request.POST)
        if form.is_valid():
            item = form.save()
            return redirect('item_detail', pk=item.id)
    else:
        form = ItemForm()

    return render(request, 'template.html', {'form': form})
```

### Form in Template

```django
<form method="post">
    {% csrf_token %}
    {{ form.as_p }}
    <button type="submit">Submit</button>
</form>
```

## Available Forms

Forms are defined in `forms.py` and provide:

- **Field validation** - Server-side validation of input
- **Widget customization** - HTML rendering and attributes
- **Error messages** - Clear error messages for invalid input
- **Help text** - Guidance for users on each field

## Validation

### Field Validation

Each field has built-in validation:

```python
class ItemForm(forms.ModelForm):
    email = forms.EmailField()
    age = forms.IntegerField(min_value=0, max_value=150)

    class Meta:
        model = Item
        fields = ['name', 'email', 'age']
```

### Custom Validation

```python
class ItemForm(forms.ModelForm):
    def clean_name(self):
        name = self.cleaned_data['name']
        if len(name) < 2:
            raise forms.ValidationError('Name too short')
        return name

    def clean(self):
        cleaned_data = super().clean()
        if condition:
            raise forms.ValidationError('Error message')
        return cleaned_data
```

## Form Usage

### Validate User Input

```python
form = ItemForm(request.POST)
if form.is_valid():
    name = form.cleaned_data['name']
    email = form.cleaned_data['email']
else:
    errors = form.errors
    field_error = form.errors['field_name']
```

### Create Form Instance

```python
# Empty form
form = ItemForm()

# With initial data
form = ItemForm(initial={'name': 'Default'})

# With POST data
form = ItemForm(request.POST)

# With instance (update)
item = Item.objects.get(id=1)
form = ItemForm(instance=item)
```

## Best Practices

1. **Always validate** - Never trust user input
2. **Clear error messages** - Provide helpful validation feedback
3. **Use ModelForm** - For forms tied to Django models
4. **CSRF protection** - Always include {% csrf_token %}
5. **Test validation** - Test all validation rules
6. **Sanitize input** - Use Django built-in cleaning
7. **Help text** - Provide guidance for complex fields

## Related Modules

- `django.forms` - Django forms framework
- `django.forms.models` - ModelForm
- Parent module documentation