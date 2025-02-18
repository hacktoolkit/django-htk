"""Custom social backends

These can be removed when various social-core pull requests are merged.
"""

# Django Extensions Imports
from social_core.backends.oauth import BaseOAuth2


class WithingsOAuth2(BaseOAuth2):
    """Withings OAuth2 authentication backend"""

    name = 'withings'
    AUTHORIZATION_URL = 'https://account.withings.com/oauth2_user/authorize2'
    REQUEST_TOKEN_URL = 'https://wbsapi.withings.net/v2/oauth2'
    ACCESS_TOKEN_URL = 'https://wbsapi.withings.net/v2/oauth2'
    ACCESS_TOKEN_METHOD = 'POST'
    ID_KEY = 'userid'

    EXTRA_DATA = [
        ('scope', 'scope'),
        ('refresh_token', 'refresh_token'),
        ('expires_in', 'expires'),
    ]

    DEFAULT_SCOPE = [
        'user.info',
        'user.metrics',
        'user.activity',
    ]
    SCOPE_SEPARATOR = ','

    def auth_complete_params(self, state=None):
        params = super().auth_complete_params(state)
        params['action'] = 'requesttoken'
        return params

    def request_access_token(self, *args, **kwargs):
        response = super().request_access_token(*args, **kwargs)
        if 'error' not in response and 'body' in response:
            # not an error, hoist response.body to top level
            response.update(response['body'])
        return response

    def get_user_details(self, response):
        return {}
