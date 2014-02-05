from django import forms

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
