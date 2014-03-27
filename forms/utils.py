from django import forms

from htk.utils import htk_setting

TEXT_STYLE_INPUTS = (
    forms.TextInput,
    forms.EmailInput,
    forms.PasswordInput,
    forms.Textarea,
    forms.URLInput,
)

def clean_model_instance_field(form_obj, field_name, cls):
    """Called from within the clean method of a ModelInstanceField or CharField
    `form_obj` is the instance of the Form
    `field_name` is the key of the field
    `cls` is the class of the underlying Model of the field
    """
    data = form_obj.cleaned_data[field_name]
    if not data:
        raise forms.ValidationError()
    try:
        instance = cls.objects.get(id=data)
    except cls.DoesNotExist:
        raise forms.ValidationError()
    return instance

def set_input_attrs(form, attrs=None):
    """Set various attributes on form input fields
    """
    for name, field in form.fields.items():
        if field.widget.__class__ in TEXT_STYLE_INPUTS:
            field.widget.attrs['class'] = getattr(attrs, 'class', htk_setting('HTK_DEFAULT_FORM_INPUT_CLASS'))
        if field.required:
            field.widget.attrs['required'] = 'required'

def set_input_placeholder_labels(form):
    """Set placeholder attribute to the field label on form input fields, if it doesn't have a placeholder set
    """
    for name, field in form.fields.items():
        if field.widget.__class__ in TEXT_STYLE_INPUTS:
            if not field.widget.attrs.get('placeholder'):
                field.widget.attrs['placeholder'] = field.label

def get_form_errors(form):
    """Return a list of errors on the form

    `form` is already known to be invalid,
    e.g. form.is_valid() == False
    """
    all_errors = []
    all_field_errors = []
    for error in form.non_field_errors():
        errors.append(error)
    for field in form:
        if field.errors:
            field_errors = (field.name, field.errors,)
            all_field_errors.append(field_errors)
    return (all_errors, all_field_errors,)
