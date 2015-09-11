from django.contrib import admin
from django.contrib.auth import get_user_model

from social.apps.django_app.default.models import UserSocialAuth

from htk.apps.accounts.models import UserAttribute
from htk.apps.accounts.models import UserEmail
from htk.apps.accounts.utils.general import get_user_profile_model

class UserProfileInline(admin.StackedInline):
    model = get_user_profile_model()
    can_delete = False
    filter_horizontal = (
    )

class UserAttributeInline(admin.TabularInline):
    model = UserAttribute
    extra = 0
    can_delete = True

class UserEmailInline(admin.TabularInline):
    model = UserEmail
    extra = 0
    can_delete = True

class UserSocialAuthInline(admin.TabularInline):
    model = UserSocialAuth
    extra = 0
    can_delete = True
