from django.contrib.auth import get_user_model

from htk.apps.accounts.utils.general import get_user_profile_model

def create_missing_user_profiles():
    """Create missing user profiles
    """
    UserModel = get_user_model()
    UserProfileModel = get_user_profile_model()
    if UserProfileModel:
        users_without_profiles = UserModel.objects.filter(
            profile=None
        )
        for user in users_without_profiles:
            profile = UserProfileModel.objects.create(
                user = user
            )
