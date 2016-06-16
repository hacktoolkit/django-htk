import base64
import requests
import rollbar

from htk.lib.fitbit.constants import *

class FitbitAPI(object):
    """
    https://dev.fitbit.com/docs/
    """
    def __init__(self, social_auth_user, client_id, client_secret):
        """Constructor for FitbitAPI

        `social_auth_user` a python-social-auth object
        `client_id` OAuth2 Client Id from Fitbit App settings
        `client_secret` OAuth2 Client Secret from Fitbit App settings
        """
        self.social_auth_user = social_auth_user
        self.client_id = client_id
        self.client_secret = client_secret

    def get_resource_url(self, resource_type):
        """Returns the resource URL for `resource_type`
        """
        url = '%s%s' % (
            FITBIT_API_BASE_URL,
            FITBIT_API_RESOURCES.get(resource_type),
        )
        return url

    def make_headers(self, auth_type, headers=None):
        """Make headers for Fitbit API request
        `auth_type` the string 'basic' or 'bearer'

        https://dev.fitbit.com/docs/basics/#language
        """
        if auth_type == 'bearer':
            auth_header = 'Bearer %s' % self.social_auth_user.extra_data['access_token']
        else:
            auth_header = 'Basic %s' % base64.b64encode('%s:%s' % (self.client_id, self.client_secret,))
        _headers = {
            'Authorization' : auth_header,
            'Accept-Locale' : 'en_US',
            'Accept-Language' : 'en_US',
        }
        if headers:
            _headers.update(headers)
        headers = _headers
        return headers

    def get(self, resource_type, params, headers=None, auth_type='bearer', refresh_token=True):
        """Performs a Fitbit API GET request
        `auth_type` the string 'basic' or 'bearer'
        `refresh_token` if True, will refresh the OAuth token when needed
        """
        url = self.get_resource_url(resource_type)
        headers = self.make_headers(auth_type, headers=headers)
        response = requests.get(url, headers=headers, params=params)
        if response.status_code == 401:
            if False and refresh_token:
                was_refreshed = self.refresh_oauth2_token()
                if was_refreshed:
                    # if token was successfully refreshed, repeat request
                    response = self.get(resource_type, params, auth_type=auth_type, refresh_token=False)
                else:
                    pass
            else:
                extra_data = {
                    'user_id' : self.social_auth_user.user.id,
                    'username' : self.social_auth_user.user.username,
                    'response' : response.json(),
                }
                rollbar.report_message('Fitbit OAuth token expired, needs refreshing', extra_data=extra_data)
        elif response.status_code == 200:
            pass
        else:
            extra_data = {
                'response' : response.json(),
            }
            rollbar.report_message('Unexpected response from Fitbit API GET request', extra_data=extra_data)

        return response

    def post(self, resource_type, params, headers=None, auth_type='bearer'):
        """Performs a Fitbit API POST request
        `auth_type` the string 'basic' or 'bearer'
        """
        url = self.get_resource_url(resource_type)
        headers = self.make_headers(auth_type, headers=headers)
        response = requests.post(url, headers=headers, params=params)
        return response

    ##
    # Permissions API calls

    def refresh_oauth2_token(self):
        params = {
            'grant_type' : 'refresh_token',
            'refresh_token' : self.social_auth_user.extra_data['refresh_token'],
        }
        headers = {
            'Content-Type' : 'application/x-www-form-urlencoded',
        }
        response = self.post('refresh', params, headers=headers, auth_type='basic')
        if response.status_code == 200:
            response_json = response.json()
            self.social_auth_user.extra_data.update(response_json)
            self.social_auth_user.save()
            was_refreshed = True
        else:
            was_refreshed = False
            extra_data = {
                'user_id' : self.social_auth_user.user.id,
                'username' : self.social_auth_user.user.username,
                'response' : response.json(),
            }
            rollbar.report_message('Unable to refresh Fitbit OAuth2.0 token', extra_data=extra_data)
        return was_refreshed

    def revoke_access(self):
        params = {
            'token' : self.social_auth_user.extra_data['access_token'],
        }
        response = self.post('revoke', params, 'basic')
        if response.status_code == 200:
            was_revoked = True
        else:
            was_revoked = False
        return was_revoked

    ##
    # Regular API calls

    def get_devices(self):
        params = {}
        response = self.get('devices', params)
        if response.status_code == 200:
            devices = response.json()
        else:
            devices = []
        return devices
