# Third Party (PyPI) Imports
import requests
import rollbar

# HTK Imports
from htk.compat import b64encode
from htk.lib.fitbit.constants import (
    FITBIT_API_BASE_URL,
    FITBIT_API_RESOURCES,
)
from htk.utils import (
    refresh,
    utcnow,
)


# isort: off


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
        self.user = social_auth_user.user
        self.social_auth_user = social_auth_user
        self.client_id = client_id
        self.client_secret = client_secret

    def get_resource_url(self, resource_type, resource_args=None):
        """Returns the resource URL for `resource_type`"""
        resource_path = FITBIT_API_RESOURCES.get(resource_type)
        if resource_args:
            resource_path = resource_path(*resource_args)

        url = '%s%s' % (
            FITBIT_API_BASE_URL,
            resource_path,
        )
        return url

    def make_headers(self, auth_type, headers=None):
        """Make headers for Fitbit API request
        `auth_type` the string 'basic' or 'bearer'

        https://dev.fitbit.com/docs/basics/#language
        """
        # refreshes token if necessary
        if self.social_auth_user.access_token_expired():
            from social_django.utils import load_strategy

            access_token = self.social_auth_user.get_access_token(
                load_strategy()
            )
            self.social_auth_user = refresh(self.social_auth_user)

        if auth_type == 'bearer':
            auth_header = (
                'Bearer %s' % self.social_auth_user.extra_data['access_token']
            )
        else:
            basic_value = '%s:%s' % (
                self.client_id,
                self.client_secret,
            )
            auth_header = 'Basic %s' % b64encode(basic_value)
            if isinstance(auth_header, bytes):
                auth_header = auth_header.decode('utf-8')
        _headers = {
            'Authorization': auth_header,
            'Accept-Locale': 'en_US',
            'Accept-Language': 'en_US',
        }
        if headers:
            _headers.update(headers)
        headers = _headers
        return headers

    def get(
        self,
        resource_type,
        resource_args=None,
        params=None,
        headers=None,
        auth_type='bearer',
        refresh_token=True,
    ):
        """Performs a Fitbit API GET request
        `auth_type` the string 'basic' or 'bearer'
        `refresh_token` if True, will refresh the OAuth token when needed
        """
        url = self.get_resource_url(resource_type, resource_args=resource_args)

        if headers is None:
            headers = self.make_headers(auth_type, headers=headers)

        response = requests.get(url, headers=headers, params=params)

        if response.status_code == 401:
            # TODO: deprecate. should proactively refresh
            if refresh_token:
                was_refreshed = self.refresh_oauth2_token()
                if was_refreshed:
                    # if token was successfully refreshed, repeat request
                    response = self.get(
                        resource_type,
                        resource_args=resource_args,
                        params=params,
                        headers=headers,
                        auth_type=auth_type,
                        refresh_token=False,
                    )
                else:
                    pass
            else:
                extra_data = {
                    'user_id': self.social_auth_user.user.id,
                    'username': self.social_auth_user.user.username,
                    'response': response.json(),
                }
                rollbar.report_message(
                    'Fitbit OAuth token expired, needs refreshing',
                    extra_data=extra_data,
                )
        elif response.status_code == 200:
            pass
        else:
            extra_data = {
                'response': response.json(),
            }
            rollbar.report_message(
                'Unexpected response from Fitbit API GET request',
                extra_data=extra_data,
            )

        return response

    def post(
        self,
        resource_type,
        resource_args=None,
        params=None,
        headers=None,
        auth_type='bearer',
    ):
        """Performs a Fitbit API POST request
        `auth_type` the string 'basic' or 'bearer'
        """
        url = self.get_resource_url(resource_type, resource_args=resource_args)
        headers = self.make_headers(auth_type, headers=headers)
        response = requests.post(url, headers=headers, params=params)
        return response

    ##################################################
    # Permissions API calls

    def refresh_oauth2_token(self):
        # TODO: deprecate
        params = {
            'grant_type': 'refresh_token',
            'refresh_token': self.social_auth_user.extra_data['refresh_token'],
        }
        headers = {
            'Content-Type': 'application/x-www-form-urlencoded',
        }
        response = self.post(
            'refresh', params, headers=headers, auth_type='basic'
        )
        if response.status_code == 200:
            response_json = response.json()
            self.social_auth_user.extra_data.update(response_json)
            self.social_auth_user.save()
            was_refreshed = True
        else:
            was_refreshed = False
            extra_data = {
                'user_id': self.social_auth_user.user.id,
                'username': self.social_auth_user.user.username,
                'response': response.json(),
            }
            rollbar.report_message(
                'Unable to refresh Fitbit OAuth2.0 token', extra_data=extra_data
            )
        return was_refreshed

    def revoke_access(self):
        params = {
            'token': self.social_auth_user.extra_data['access_token'],
        }
        response = self.post('revoke', params, 'basic')
        if response.status_code == 200:
            was_revoked = True
        else:
            was_revoked = False
        return was_revoked

    ##################################################
    # Regular API calls

    ##
    # Activity
    # https://dev.fitbit.com/build/reference/web-api/activity/

    def get_activity_steps_past_month(self):
        """Get Steps for past month

        Requires the 'activity' permission'
        https://dev.fitbit.com/docs/activity/
        """
        response = self.get('activity-steps-monthly')
        if response.status_code == 200:
            activity = response.json()['activities-steps']
            activity = activity[::-1]
        else:
            activity = None
        return activity

    ##
    # Body & Weight
    # https://dev.fitbit.com/build/reference/web-api/body/

    def get_body_fat_logs(self, dt=None):
        """Get Body Fat logs for a given date"""
        if dt is None:
            dt = utcnow()

        resource_args = (dt.strftime('%Y-%m-%d'),)
        response = self.get('fat', resource_args=resource_args)
        if response.status_code == 200:
            fat_logs = response.json()['fat']
            fat_logs = fat_logs[::-1]
        else:
            fat_logs = None
        return fat_logs

    def get_body_fat_logs_past_day(self):
        fat_logs = self.get_body_fat_logs()
        return fat_logs

    def get_weight_logs(self, dt=None):
        """Get Weight logs for a given date"""
        if dt is None:
            dt = utcnow()

        resource_args = (dt.strftime('%Y-%m-%d'),)
        response = self.get('weight', resource_args=resource_args)
        if response.status_code == 200:
            weight_logs = response.json()['weight']
            weight_logs = weight_logs[::-1]
        else:
            weight_logs = None
        return weight_logs

    def get_weight_logs_past_day(self):
        weight_logs = self.get_weight_logs()
        return weight_logs

    def get_most_recent_weight(self):
        weight_logs = self.get_weight_logs_past_day()
        weight_log = weight_logs[0]
        return weight_log

    ##
    # Devices
    # https://dev.fitbit.com/build/reference/web-api/devices/

    def get_devices(self):
        """Get a list of Devices

        Requires the 'settings' permission
        https://dev.fitbit.com/docs/devices/
        """
        response = self.get('devices')
        if response.status_code == 200:
            devices = response.json()
        else:
            devices = []
        return devices
