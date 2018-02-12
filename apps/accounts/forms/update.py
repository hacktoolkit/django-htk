import re
import rollbar

from django import forms
from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import SetPasswordForm

from htk.apps.accounts.emails import password_changed_email
from htk.forms import AbstractModelInstanceUpdateForm
from htk.forms.utils import set_input_attrs
from htk.forms.utils import set_input_placeholder_labels
from htk.utils import htk_setting
from htk.utils import resolve_model_dynamically
from htk.utils.geo import get_us_state_abbreviation_choices

UserModel = get_user_model()
UserProfile = resolve_model_dynamically(settings.AUTH_PROFILE_MODULE)

class UserUpdateForm(AbstractModelInstanceUpdateForm):
    class Meta:
        model = UserModel
        exclude = (
            # these fields should never be manipultated from this form
            'email', # managed by UserEmail objects
            'password',
        )

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
        ProfileFormClass = kwargs.pop('profile_form_class', UserProfileUpdateForm)
        super(UserUpdateForm, self).__init__(user, *args, **kwargs)
        self.profile_form = ProfileFormClass(user_profile, *args, **kwargs)

    def has_username_field(self):
        """Determines whether username is a field in this form instance
        """
        result = 'username' in self._save_fields
        return result

    def clean_username(self):
        """If username is a field in this form instance, ensure that it satisfies the regular expression
        """
        if self.has_username_field():
            username = self.cleaned_data.get('username', '').strip()
            matches = re.match(htk_setting('HTK_VALID_USERNAME_REGEX'), username)
            if matches is None:
                raise forms.ValidationError('There are invalid characters in the username.')
            else:
                pass
        else:
            username = None
        return username

    def get_profile_form(self):
        profile_form = self.profile_form
        return profile_form

    def save(self, *args, **kwargs):
        user = super(UserUpdateForm, self).save(*args, **kwargs)
        if self.has_username_field():
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
        exclude = (
            'has_username_set',
        )
        widgets = {
            'state': forms.widgets.Select(choices=get_us_state_abbreviation_choices()),
        }

class ChangeUsernameForm(UserUpdateForm):
    class Meta:
        model = UserModel
        fields = (
            'username',
        )
        help_texts = {
            'username' : 'Usernames can only contain alphanumerics (letters (a-z) or digits (0-9)), underscores (_), and hyphens (-).',
        }

class ChangePasswordForm(SetPasswordForm):
    def __init__(self, *args, **kwargs):
        super(ChangePasswordForm, self).__init__(*args, **kwargs)
        self.fields['new_password2'].label = 'Confirm new password'
        set_input_attrs(self)
        set_input_placeholder_labels(self)

    def save(self, user, *args, **kwargs):
        user = super(ChangePasswordForm, self).save(*args, **kwargs)
        try:
            password_changed_email(user)
        except:
            from htk.utils.request import get_current_request
            request = get_current_request()
            extra_data = {
                'user' : user,
                'email' : user.email,
            }
            rollbar.report_exc_info(request=request, extra_data=extra_data)
        return user
