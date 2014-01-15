from django import forms

from htk.apps.prelaunch.emails import prelaunch_email
from htk.apps.prelaunch.models import PrelaunchSignup

class PrelaunchSignupForm(forms.ModelForm):
    class Meta:
        model = PrelaunchSignup
        fields = (
            'email',
        )

    def save(self, site, commit=False, *args, **kwargs):
        prelaunch_signup = super(PrelaunchSignupForm, self).save(commit=False, *args, **kwargs)
        prelaunch_signup.site = site
        prelaunch_signup.save()
        prelaunch_email(prelaunch_signup)
        return prelaunch_signup
