# Django Imports
from django.contrib.auth import (
    authenticate,
    logout,
)
from django.http import HttpResponse
from django.utils.deprecation import MiddlewareMixin

# Django Extensions Imports
from social_django.middleware import SocialAuthExceptionMiddleware

# HTK Imports
from htk.api.utils import json_response_forbidden
from htk.apps.accounts.utils.auth import login_authenticated_user
from htk.apps.accounts.utils.general import (
    authenticate_user_by_basic_auth_credentials,
)
from htk.utils import htk_setting
from htk.utils.request import parse_authorization_header


# isort: off


class BaseHtkAuthMiddleware(MiddlewareMixin):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Instance attribute to determine whether in explicit authorization flow
        self.is_explicit_auth = False

    def _handle_auth_flow(self, request, auth_user=None):
        """Performs authentication flow with `auth_user`

        Helper function for `self.process_request`

        Checks for any security violations and proceeds to log in `auth_user`
        if everything is kosher.

        The following security violations are checked:
        - Explicit authorization requested, but invalid token user
        - Implicit/explicit authorization, but mismatching users

        Side effects:
        - Logs in `auth_user` if flow is valid
        - Logs out of current session if flow is detected to be invalid
        """
        already_logged_in_user = (
            request.user
            if hasattr(request, 'user') and request.user.is_authenticated
            else None
        )

        if already_logged_in_user:
            # there was already a logged in user.
            if (
                # explicit authorization requested, invalid `auth_user`
                (self.is_explicit_auth and auth_user is None)
                # (im/ex)plicit authorization requested, but mismatching users
                or (
                    auth_user is not None
                    and auth_user != already_logged_in_user
                )
            ):
                request.user = None
                # TODO: redirect user or display error?
                logout(request)
            else:
                # no security violations
                pass

        elif auth_user:
            # token user not logged in yet
            login_authenticated_user(request, auth_user)
            request.user = auth_user

        else:
            # no valid `auth_user` found, do nothing
            # `self.process_response` will determine whether request should be
            # processed regularly, or denied
            pass

    def process_request(self, request):
        # re-initialize `is_explicit_auth` as `False` for each request
        self.is_explicit_auth = False

    def process_response(self, request, response):
        """Checks whether in an explicit authorization flow

        Allows request to process normally if authorization succeeded,
        or deny request if a security violation/anomaly was detected
        """
        if self.is_explicit_auth and not hasattr(request, 'user'):
            if request.content_type == 'application/json':
                response = json_response_forbidden()
            else:
                response = HttpResponse('Forbidden', status=403)

        return response


class HtkBasicAuthMiddleware(BaseHtkAuthMiddleware):
    """Custom Authenication Middleware to allow logging in using
    Basic authorization in HTTP headers.
    """

    def process_request(self, request):
        super().process_request(request)

        token_type, credentials = parse_authorization_header(request)

        if token_type == 'Basic':
            self.is_explicit_auth = True
            auth_user = authenticate_user_by_basic_auth_credentials(
                request, credentials
            )
        else:
            # Not Basic auth.
            # Give a chance for other auth middlewares to work.
            self.is_explicit_auth = False
            auth_user = None

        self._handle_auth_flow(request, auth_user)


class HtkUserTokenAuthMiddleware(BaseHtkAuthMiddleware):
    """Custom Authentication Middleware to attempt logging in with
    a securely generated token.

    Tokens are checked in the following order:
    - HTTP `Authorization` header
    - URL Parameter `token`

    See:
    - htk.apps.accounts.backends.HtkUserTokenAuthBackend
    - htk.apps.accounts.utils.validate_user_token_auth_token
    """

    def process_request(self, request):
        super().process_request(request)

        token_type, token = parse_authorization_header(request)

        if token_type == 'Bearer':
            # The token is in the `Authorization` header
            self.is_explicit_auth = True
            auth_user = authenticate(request=request, token=token)

        elif 'token' in request.GET:
            # Implicit authentication using URL params
            self.is_explicit_auth = True
            token = request.GET['token']
            auth_user = authenticate(request=request, token=token)

        else:
            # Give a chance for other auth middlewares to work
            self.is_explicit_auth = False
            auth_user = None

        self._handle_auth_flow(request, auth_user)


class HtkSocialAuthExceptionMiddleware(SocialAuthExceptionMiddleware):
    def get_redirect_uri(self, request, exception):
        """Redirect to LOGIN_ERROR_URL by default
        Otherwise, go to the SOCIAL_AUTH_<STRATEGY>_LOGIN_ERROR_URL for that backend
        provider if specified.

        However, if user is logged in when the exception occurred,
        it is a connection failure.
        Therefore, always go to account settings page or equivalent.
        """
        default_url = super(
            HtkSocialAuthExceptionMiddleware, self
        ).get_redirect_uri(request, exception)
        if request.user.is_authenticated:
            url = htk_setting('HTK_SOCIAL_AUTH_CONNECT_ERROR_URL', default_url)
        else:
            url = default_url
        return url
