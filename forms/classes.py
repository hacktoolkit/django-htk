from django import forms

from htk.forms.utils import set_input_attrs
from htk.forms.utils import set_input_placeholder_labels
from htk.utils.cache_descriptors import CachedAttribute

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
        self.attrs = kwargs.pop('attrs', {})
        self.use_react = kwargs.pop('use_react', False)
        self.instance = instance
        super(AbstractModelInstanceUpdateForm, self).__init__(instance=instance, *args, **kwargs)
        self._set_save_fields(*args)

        if args or kwargs:
            # make all non-save fields optional
            for name, field in self.fields.items():
                if name not in self._save_fields_lookup:
                    field.required = False
                else:
                    pass
        else:
            # leave the fields the way they are for rendering a form initially
            pass
        set_input_attrs(self)
        set_input_placeholder_labels(self)

    def _set_save_fields(self, *args, **kwargs):
        """Determine the subset of fields that we want to save

        Called by self.__init__()
        """
        save_fields_lookup = kwargs.pop('save_fields_lookup', {})
        for arg in args:
            if hasattr(arg, '__iter__'):
                # arg is an iterable
                # e.g. QueryDict from request.POST or request.FILES
                for key, value in arg.items():
                    # only save this field if it is recognized in both this form and the model instance
                    if key in self.fields and hasattr(self.instance, key):
                        save_fields_lookup[key] = True
                    else:
                        pass
            else:
                pass
        self._save_fields_lookup = save_fields_lookup
        self._save_fields = save_fields_lookup.keys()

    def save(self, commit=True, should_refresh=True, *args, **kwargs):
        """Saves this form

        `should_refresh` whether the instance is a limited or full instance. Default True.
        This is slightly less performant, but ensures less confusing behavior, and is less prone to human error.

        Returns an updated instance

        Caveat emptor! If not refreshed, instance returned will be a limited instance
        Subsequently calling save() on the returned instance could clear out other fields if not called with update_fields

        It is recommended to refresh the instance to get the entire object, not one with limited fields in memory

        The instance can be refreshed by doing such:
        instance = instance.__class__.objects.get(id=instance.id)
        """
        instance = self.instance
        if instance is None or instance.id is None:
            # in case there is not an instance, create a new one
            instance = super(AbstractModelInstanceUpdateForm, self).save(commit=commit, *args, **kwargs)
            return instance
        for field in self._save_fields:
            if field in self.cleaned_data:
                value = self.cleaned_data[field]
                instance.__setattr__(field, value)
        if commit:
            instance.save(update_fields=self._save_fields)
            if should_refresh:
                from htk.utils.general import refresh
                instance = refresh(instance)
        return instance

class AbstractModelInstanceAttributesFormMixin(object):
    def __init__(self, instance):
        self.instance = instance
        initial = self.get_initial_values_from_instance(instance)
        self.initial = initial

    @CachedAttribute
    def instance_attribute_fields(self):
        raise AbstractMethodNotImplemented()
        fields = []
        return fields

    @CachedAttribute
    def boolean_attributes_lookup(self):
        raise AbstractMethodNotImplemented()
        boolean_attributes = ()
        lookup = { k : True for k in boolean_attributes }
        return lookup

    def get_initial_values_from_instance(self, instance):
        attributes = self.instance_attribute_fields
        boolean_attributes = self.boolean_attributes_lookup
        initial_values = {
            k : instance.get_attribute(k, as_bool=k in boolean_attributes)
            for k
            in attributes
        }
        return initial_values

    def save_instance_attributes(self):
        instance = self.instance
        initial_values = self.initial
        boolean_attributes = self.boolean_attributes_lookup
        was_updated = False
        for key, old_value in initial_values.iteritems():
            new_value = self.cleaned_data.get(key, '')
            if type(new_value) == str:
                new_value = new_value.strip()
            if new_value != old_value:
                instance.set_attribute(key, new_value, as_bool=key in boolean_attributes)
                was_updated = True
            else:
                pass
        return was_updated

class AbstractModelInstanceAttributesForm(forms.Form, AbstractModelInstanceAttributesFormMixin):
    def __init__(self, instance, *args, **kwargs):
        AbstractModelInstanceAttributesFormMixin.__init__(self, instance)
        kwargs['initial'] = self.initial
        forms.Form.__init__(self, *args, **kwargs)

    def save(self):
        was_updated = self.save_instance_attributes()
        return was_updated

class AbstractModelInstanceUpdateFormWithAttributes(
    AbstractModelInstanceUpdateForm,
    AbstractModelInstanceAttributesFormMixin
):
    def __init__(self, instance, *args, **kwargs):
        AbstractModelInstanceAttributesFormMixin.__init__(self, instance)
        kwargs['initial'] = self.initial
        AbstractModelInstanceUpdateForm.__init__(self, instance, *args, **kwargs)

    def save(self):
        #updated_instance = AbstractModelInstanceAttributesForm.save(self)
        updated_instance = super(AbstractModelInstanceUpdateFormWithAttributes, self).save(self)
        attributes_updated = self.save_instance_attributes()
        return updated_instance
