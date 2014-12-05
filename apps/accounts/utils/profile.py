from django.contrib.auth import get_user_model

from htk.utils import htk_setting
from htk.utils.general import resolve_model_dynamically

def create_missing_user_profiles():
    """Create missing user profiles
    """
    UserModel = get_user_model()
    user_profile_model_name = htk_setting('HTK_USER_PROFILE_MODEL')
    UserProfileModel = resolve_model_dynamically(user_profile_model_name)
    if UserProfileModel:
        users_without_profiles = UserModel.objects.filter(
            profile=None
        )
        for user in users_without_profiles:
            profile = UserProfileModel.objects.create(
                user = user
            )
