from social.apps.django_app.default.models import UserSocialAuth

def get_social_auth_for_user(user, provider):
    """Get UserSocialAuth for given `user` and `provider`

    Returns None if not found
    """
    try:
        social = user.social_auth.get(
            provider=provider
        )
    except UserSocialAuth.DoesNotExist:
        social = None
    return social
