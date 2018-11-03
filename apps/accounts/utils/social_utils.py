def get_social_auth_for_user(user, provider):
    """Get one UserSocialAuth for given `user` and `provider`

    Returns None if not found
    """
    social_users = get_social_auths_for_user(user, provider=provider)
    if social_users.exists():
        social_user = social_users.first()
    else:
        social_user = None
    return social_user


def get_social_auths_for_user(user, provider=None):
    """Get UserSocialAuths for given `user`

    Filter by specific `provider` if set

    Returns a QuerySet of UserSocialAuth objects
    """
    social_users = user.social_auth
    if provider is None:
        social_users = social_users.all()
    else:
        social_users = social_users.filter(
            provider=provider
        )
    return social_users
