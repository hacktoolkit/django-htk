from django import forms
from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import SetPasswordForm

from htk.forms import AbstractModelInstanceUpdateForm
from htk.forms.utils import set_input_attrs
from htk.forms.utils import set_input_placeholder_labels
from htk.utils import resolve_model_dynamically
from htk.utils.geo import get_us_state_abbreviation_choices

UserModel = get_user_model()
UserProfile = resolve_model_dynamically(settings.AUTH_PROFILE_MODULE)

class UserUpdateForm(AbstractModelInstanceUpdateForm):
    class Meta:
        model = UserModel

    def __init__(self, instance, *args, **kwargs):
        user = instance
        user_profile = user.profile
        if not args and not kwargs:
            # override the displayed username value if not set by the user yet
            # only do this for rendering a form initially (i.e. no request.POST)
            username_field_display_value = user.username if user_profile.has_username_set else ''
            user.username = username_field_display_value
        else:
            pass
        super(UserUpdateForm, self).__init__(user, *args, **kwargs)
        self.profile_form = UserProfileUpdateForm(user_profile, *args, **kwargs)

    def get_profile_form(self):
        profile_form = self.profile_form
        return profile_form

    def save(self, *args, **kwargs):
        user = super(UserUpdateForm, self).save(*args, **kwargs)
        if 'username' in self.save_fields:
            user_profile = user.profile
            user_profile.has_username_set = True
            user_profile.save(update_fields=['has_username_set',])
            user = user_profile.user
        else:
            pass
        return user
        
class UserProfileUpdateForm(AbstractModelInstanceUpdateForm):
    class Meta:
        model = UserProfile
        widgets = {
            'state': forms.widgets.Select(choices=get_us_state_abbreviation_choices()),
        }

class ChangePasswordForm(SetPasswordForm):
    def __init__(self, *args, **kwargs):
        super(ChangePasswordForm, self).__init__(*args, **kwargs)
        self.fields['new_password2'].label = 'Confirm new password'
        set_input_attrs(self)
        set_input_placeholder_labels(self)
