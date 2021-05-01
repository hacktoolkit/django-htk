# Third Party (PyPI) Imports
import rollbar

# Django Imports
from django import forms

# HTK Imports
from htk.apps.prelaunch.emails import prelaunch_email
from htk.apps.prelaunch.models import PrelaunchSignup
from htk.forms.utils import (
    set_input_attrs,
    set_input_placeholder_labels,
)
from htk.utils import htk_setting


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

        if htk_setting('HTK_SLACK_NOTIFICATIONS_ENABLED'):
            from htk.utils.notifications import slack_notify
            try:
                message = '{} <{}> just signed up for the pre-launch waiting list.'.format(
                    prelaunch_signup.full_name,
                    prelaunch_signup.email
                )
                slack_notify(message)
            except:
                rollbar.report_exc_info()
        else:
            pass

        try:
            prelaunch_email(prelaunch_signup)
        except Exception:
            rollbar.report_exc_info()

        return prelaunch_signup
