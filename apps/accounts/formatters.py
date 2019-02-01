"""Formatter functions for User object
"""

def format_suggest_username(user):
    """Returns only the username
    """
    obj = {
        'username' : user.username,
    }
    return obj

def format_suggest_username_name(user):
    from htk.lib.gravatar.utils import get_gravatar_hash
    obj = {
        'username' : user.username if user.profile.has_username_set else '',
        'first_name' : user.first_name.strip(),
        'last_name' : user.last_name.strip(),
        'display_name' : user.profile.get_display_name(),
        'gravatar_hash' : get_gravatar_hash(user.profile.confirmed_email or user.email),
    }
    return obj

DEFAULT_USER_SUGGEST_FORMATTER = format_suggest_username_name
