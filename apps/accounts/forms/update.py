from django import forms
from django.conf import settings
from django.contrib.auth import get_user_model

from htk.apps.accounts.models import AbstractUserProfile
from htk.utils import resolve_model_dynamically
from htk.utils.geo import get_us_state_abbreviation_choices

UserModel = get_user_model()
UserProfile = resolve_model_dynamically(settings.AUTH_PROFILE_MODULE)

class AbstractUpdateUserForm(forms.ModelForm):
    def __init__(self, user, *args, **kwargs):
        self.user = user
        super(AbstractUpdateUserForm, self).__init__(*args, **kwargs)

    def get_user_obj(self):
        if self.user:
            user_obj = self.user
        else:
            user_obj = None
        return user_obj

    def save(self, commit=True):
        user_obj = self.get_user_obj()
        if user_obj and self.fields:
            for field in self.fields:
                value = self.cleaned_data[field]
                user_obj.__setattr__(field, value)
            user_obj.save(update_fields=self.fields)
        return user_obj

class AbstractUpdateUserProfileForm(AbstractUpdateUserForm):
    def get_user_obj(self):
        if self.user:
            user_obj = self.user.profile
        else:
            user_obj = None
        return user_obj

class UpdateUsernameForm(AbstractUpdateUserForm):
    class Meta:
        model = UserModel
        fields = ('username',)

    def save(self, commit=True):
        user = super(UpdateUsernameForm, self).save(commit=True)
        user_profile = user.profile
        user_profile.has_username_set = True
        user_profile.save()
        return user

class UpdateUserFirstNameForm(AbstractUpdateUserForm):
    class Meta:
        model = UserModel
        fields = ('first_name',)

class UpdateUserLastNameForm(AbstractUpdateUserForm):
    class Meta:
        model = UserModel
        fields = ('last_name',)

class UpdateUserShareNameForm(AbstractUpdateUserProfileForm):
    class Meta:
        model = UserProfile
        fields = ('share_name',)

class UpdateUserCityForm(AbstractUpdateUserProfileForm):
    class Meta:
        model = UserProfile
        fields = ('city',)

class UpdateUserStateForm(AbstractUpdateUserProfileForm):
    class Meta:
        model = UserProfile
        fields = ('state',)
        widgets = {
            'state': forms.widgets.Select(choices=get_us_state_abbreviation_choices()),
        }

class UpdateUserWebsiteForm(AbstractUpdateUserProfileForm):
    class Meta:
        model = UserProfile
        fields = ('website',)

class UpdateUserFacebookForm(AbstractUpdateUserProfileForm):
    class Meta:
        model = UserProfile
        fields = ('facebook',)

class UpdateUserTwitterForm(AbstractUpdateUserProfileForm):
    class Meta:
        model = UserProfile
        fields = ('twitter',)

class UpdateUserBiographyForm(AbstractUpdateUserProfileForm):
    class Meta:
        model = UserProfile
        fields = ('biography',)

class UpdateUserShareLocationForm(AbstractUpdateUserProfileForm):
    class Meta:
        model = UserProfile
        fields = ('share_location',)
