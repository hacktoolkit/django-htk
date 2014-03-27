from django import forms

from htk.forms.utils import set_input_placeholder_labels

class AbstractModelInstanceUpdateForm(forms.ModelForm):
    """An abstract class for manipulating Model instances

    Since this is an abstract class, it is meant to be extended

    Features:
    All fields that aren't passed in request.POST or request.FILES are optional (required=False)
    Only limited fields are saved

    This is limited-update mechanism is useful for API endpoints that only update one or a few fields on a model instance instead of the entire object
    """
    def __init__(self, instance, *args, **kwargs):
        """Overrides forms.ModelForm.__init__()
        Unlike forms.ModelForm, instance is required
        """
        self.instance = instance
        save_fields = []
        for arg in args:
            if hasattr(arg, '__iter__'):
                # arg is an iterable
                # e.g. QueryDict from request.POST or request.FILES
                for key, value in arg.items():
                    if hasattr(instance, key):
                        save_fields.append(key)
                    else:
                        pass
            else:
                pass
        self.save_fields = save_fields
        save_fields_dict = dict(zip(save_fields, [True] * len(save_fields)))
        super(AbstractModelInstanceUpdateForm, self).__init__(instance=instance, *args, **kwargs)
        # make all non-save fields optional
        for name, field in self.fields.items():
            if name not in save_fields_dict:
                field.required = False
        set_input_placeholder_labels(self)

    def save(self, commit=True):
        """Saves this form

        Returns an updated instance
        """
        instance = self.instance
        for field in self.save_fields:
            value = self.cleaned_data[field]
            instance.__setattr__(field, value)
        instance.save(update_fields=self.save_fields)
        return instance
