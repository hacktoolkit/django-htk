import pytz

from django import forms
from django.conf import settings

from htk.session_keys import *
from htk.utils import htk_setting
from htk.utils import resolve_model_dynamically

UserProfile = resolve_model_dynamically(settings.AUTH_PROFILE_MODULE)

class AddEmailForm(forms.Form):
    add_email = forms.CharField(widget=forms.HiddenInput(attrs={'value': 1}))
    email = forms.EmailField()

    def clean_email(self):
        email = self.cleaned_data['email']
        user = get_user_by_email(email)
        if user is None:
            self.email = email
        else:
            raise forms.ValidationError('This email is already registered')

    def save(self, user=None, domain=None, commit=True):
        domain = domain or htk_setting('HTK_DEFAULT_EMAIL_SENDING_DOMAIN')
        user_email = None
        if user:
            email = self.email
            user_email = associate_user_email(user, email, domain)
        return user_email
