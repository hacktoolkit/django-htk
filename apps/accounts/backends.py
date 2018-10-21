# Python Standard Library Imports

# Third Party / PIP Imports

# Django Imports
from django.contrib.auth.backends import ModelBackend

# HTK Imports
from htk.apps.accounts.utils.auth import validate_user_token_auth_token


class HtkUserTokenAuthBackend(ModelBackend):
    """Custom backend that uses a securely generated token

    Authenticates against settings.AUTH_USER_MODEL
    """
    def authenticate(self, request, token=None):
        user = None
        if token:
            token_user, is_valid = validate_user_token_auth_token(token)
            if token_user and is_valid:
                user = token_user
            else:
                # invalid token or user not found
                pass
        else:
            # missing token
            pass
        return user
