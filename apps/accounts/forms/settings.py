# Third Party (PyPI) Imports
import pytz

# Django Imports
from django import forms
from django.conf import settings

# HTK Imports
from htk.apps.accounts.utils import (
    associate_user_email,
    get_user_by_email,
)
from htk.exceptions import AbstractMethodNotImplemented
from htk.forms.utils import (
    set_input_attrs,
    set_input_placeholder_labels,
)
from htk.session_keys import *
from htk.utils import (
    htk_setting,
    resolve_model_dynamically,
)


class AddEmailForm(forms.Form):
    email = forms.EmailField(label='Email')

    def __init__(self, user=None, require_verification=True, *args, **kwargs):
        super(AddEmailForm, self).__init__(*args, **kwargs)
        self.user = user
        self.require_verification = require_verification
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
            confirmed = not self.require_verification
            user_email = associate_user_email(user, email, domain=domain, confirmed=confirmed)
        return user_email
