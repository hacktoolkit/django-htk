# Third Party (PyPI) Imports
import rollbar

# Django Imports
from django import forms

# HTK Imports
from htk.apps.prelaunch.models import PrelaunchSignup
from htk.forms.utils import (
    set_input_attrs,
    set_input_placeholder_labels,
)


# isort: off

class PrelaunchSignupForm(forms.ModelForm):
    class Meta:
        model = PrelaunchSignup
        fields = (
            'full_name',
            'email',
        )

        labels = {
            'full_name': 'Full Name',
        }

    def __init__(self, *args, **kwargs):
        super(PrelaunchSignupForm, self).__init__(*args, **kwargs)
        set_input_attrs(self)
        set_input_placeholder_labels(self)

    def save(self, site, commit=False, *args, **kwargs):
        prelaunch_signup = super(PrelaunchSignupForm, self).save(commit=False, *args, **kwargs)
        prelaunch_signup.site = site
        prelaunch_signup.save()

        prelaunch_signup.send_notifications()

        return prelaunch_signup
