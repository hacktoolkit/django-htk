import pytz

from django import forms
from django.conf import settings

from htk.apps.accounts.utils import associate_user_email
from htk.apps.accounts.utils import get_user_by_email
from htk.exceptions import AbstractMethodNotImplemented
from htk.forms.utils import set_input_attrs
from htk.forms.utils import set_input_placeholder_labels
from htk.session_keys import *
from htk.utils import htk_setting
from htk.utils import resolve_model_dynamically

class AddEmailForm(forms.Form):
    email = forms.EmailField(label='Email')

    def __init__(self, user=None, *args, **kwargs):
        super(AddEmailForm, self).__init__(*args, **kwargs)
        self.user = user
        set_input_attrs(self)
        set_input_placeholder_labels(self)

    def clean_email(self):
        email = self.cleaned_data['email']
        user = get_user_by_email(email)
        if user is None:
            self.email = email
        else:
            raise forms.ValidationError('This email is already registered')
        return email

    def save(self, domain=None, commit=True):
        user = self.user
        domain = domain or htk_setting('HTK_DEFAULT_EMAIL_SENDING_DOMAIN')
        user_email = None
        if user:
            email = self.email
            user_email = associate_user_email(user, email, domain)
        return user_email

class AbstractUserAttributesForm(forms.Form):
    def __init__(self, user, *args, **kwargs):
        self.user = user
        initial = self.get_initial_values_from_user(user)
        self.initial = initial
        kwargs['initial'] = initial
        super(AbstractUserAttributesForm, self).__init__(*args, **kwargs)
        self.label_suffix = ''
        set_input_attrs(self)
        set_input_placeholder_labels(self)
        self.cascaded_errors = []

    def get_user_attribute_fields(self):
        raise AbstractMethodNotImplemented()
        fields = []
        return fields

    def get_boolean_attributes_lookup(self):
        raise AbstractMethodNotImplemented()
        boolean_attributes = ()
        lookup = { k : True for k in boolean_attributes }
        return lookup

    def get_initial_values_from_user(self, user):
        attributes = self.get_user_attribute_fields()
        boolean_attributes = self.get_boolean_attributes_lookup()
        initial_values = {
            k : user.profile.get_attribute(k, as_bool=k in boolean_attributes)
            for k
            in attributes
        }
        return initial_values

    def save(self):
        was_updated = self.save_user_attributes()
        return was_updated

    def save_user_attributes(self):
        user = self.user
        initial_values = self.initial
        boolean_attributes = self.get_boolean_attributes_lookup()
        was_updated = False
        for key, old_value in initial_values.iteritems():
            new_value = self.cleaned_data.get(key, '')
            if type(new_value) == str:
                new_value = new_value.strip()
            if new_value != old_value:
                user.profile.set_attribute(key, new_value, as_bool=key in boolean_attributes)
                was_updated = True
            else:
                pass
        return was_updated
