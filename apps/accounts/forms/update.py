from django import forms
from django.conf import settings
from django.contrib.auth import get_user_model

from htk.forms import AbstractModelInstanceUpdateForm
from htk.utils import resolve_model_dynamically
from htk.utils.geo import get_us_state_abbreviation_choices

UserModel = get_user_model()
UserProfile = resolve_model_dynamically(settings.AUTH_PROFILE_MODULE)

class UserUpdateForm(AbstractModelInstanceUpdateForm):
    class Meta:
        model = UserModel

    def __init__(self, instance, *args, **kwargs):
        super(UserUpdateForm, self).__init__(instance, *args, **kwargs)
        self.profile_form = UserProfileUpdateForm(self.instance.profile, *args, **kwargs)

    def get_profile_form(self):
        profile_form = self.profile_form
        return profile_form
        
class UserProfileUpdateForm(AbstractModelInstanceUpdateForm):
    class Meta:
        model = UserProfile
        widgets = {
            'state': forms.widgets.Select(choices=get_us_state_abbreviation_choices()),
        }
