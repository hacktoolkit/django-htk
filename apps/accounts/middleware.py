# Python Standard Library Imports

# Django Imports
from django.contrib.auth import (
    authenticate,
    logout,
)
from django.utils.deprecation import MiddlewareMixin

# Django Extensions Imports
from social_django.middleware import SocialAuthExceptionMiddleware

# HTK Imports
from htk.apps.accounts.utils.auth import login_authenticated_user
from htk.utils import htk_setting


# isort: off


class HtkUserTokenAuthMiddleware(MiddlewareMixin):
    """Custom Authentication Middleware to attempt logging in with a securely generated token

    Tokens are checked in the following order:
    - HTTP `Authorization` header
    - URL Parameter `token`

    See:
    - htk.apps.accounts.backends.HtkUserTokenAuthBackend
    - htk.apps.accounts.utils.validate_user_token_auth_token
    """

    def process_request(self, request):
        already_logged_in_user = (
            request.user
            if hasattr(request, 'user') and request.user.is_authenticated
            else None
        )

        if 'HTTP_AUTHORIZATION' in request.META:
            # must use `Bearer` token for now
            auth_header = request.META['HTTP_AUTHORIZATION']
            parts = auth_header.split()
            if len(parts) == 2:
                method, token = parts
                if method != 'Bearer':
                    token = None
                else:
                    pass
            else:
                token = None
        elif 'token' in request.GET:
            token = request.GET['token']
        else:
            token = None

        token_user = (
            authenticate(request=request, token=token) if token else None
        )

        if token_user:
            if already_logged_in_user:
                if token_user != already_logged_in_user:
                    # mismatch between logged-in user and token user
                    logout(request)
                    # TODO: redirect user or display error?
                else:
                    # matches, do nothing
                    pass
            else:
                # token user not logged in yet
                login_authenticated_user(request, token_user)
                request.user = token_user
        else:
            # no valid user found from token, do nothing
            pass


class HtkSocialAuthExceptionMiddleware(SocialAuthExceptionMiddleware):
    def get_redirect_uri(self, request, exception):
        """Redirect to LOGIN_ERROR_URL by default
        Otherwise, go to the SOCIAL_AUTH_<STRATEGY>_LOGIN_ERROR_URL for that backend provider if specified

        However, if user is logged in when the exception occurred, it is a connection failure
        Therefore, always go to account settings page or equivalent
        """
        default_url = super(
            HtkSocialAuthExceptionMiddleware, self
        ).get_redirect_uri(request, exception)
        if request.user.is_authenticated:
            url = htk_setting('HTK_SOCIAL_AUTH_CONNECT_ERROR_URL', default_url)
        else:
            url = default_url
        return url
