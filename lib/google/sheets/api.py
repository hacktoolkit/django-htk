# Python Standard Library Imports

# Third Party (PyPI) Imports
import requests

# HTK Imports
from htk.lib.google.sheets.constants import GOOGLE_SHEETS_RESOURCES


class GoogleSheetsAuthenticationException(Exception):
    pass


class GoogleSheetsAPI(object):
    def __init__(self, user, email=None):
        self.user = user
        self.email = email
        self.g_social_auth = user.profile.get_social_user('google-oauth2', email)
        if self.g_social_auth is None:
            raise GoogleSheetsAuthenticationException()

    def get_authorization_headers(self):
        headers = {}
        if self.g_social_auth:
            # refreshes token if necessary
            if self.g_social_auth.access_token_expired():
                from social_django.utils import load_strategy
                access_token = self.g_social_auth.get_access_token(load_strategy())
                self.g_social_auth = refresh(self.g_social_auth)
            headers['Authorization'] = '%(token_type)s %(access_token)s' % self.g_social_auth.extra_data
        return headers

    def get_resource_url(self, resource_name, **kwargs):
        values = {}
        values.update(kwargs)
        url = GOOGLE_SHEETS_RESOURCES[resource_name] % values
        return url

    def do_request(self, method, resource_name, resource_args=None, headers=None, params=None, data=None, json_data=None):
        method = method.lower()
        action = getattr(requests, method, None)
        if action is None:
            raise Exception('Invalid request method specified: %s' % method)
        if resource_args is None:
            resource_args = {}
        url = self.get_resource_url(resource_name, **resource_args)
        if headers is None:
            headers = {}
        if params is None:
            params = {}
        headers.update(self.get_authorization_headers())
        response = action(url, headers=headers, params=params, data=data, json=json_data)
        return response

    ##
    # spreadsheets
    # https://developers.google.com/sheets/api/reference/rest/v4/spreadsheets

    ##
    # spreadsheets.values
    # https://developers.google.com/sheets/api/reference/rest/v4/spreadsheets.values

    def spreadsheets_values_append(self, spreadsheet_id, table_range, values, major_dimension='ROWS', value_input_option='USER_ENTERED'):
        """https://developers.google.com/sheets/api/reference/rest/v4/spreadsheets.values/append
        """
        resource_name = 'spreadsheets.values.append'
        resource_args = {
            'spreadsheet_id' : spreadsheet_id,
            'table_range' : table_range,
        }

        params = {
            'valueInputOption' : value_input_option,
        }

        json_data = {
            'values' : values,
            'majorDimension' : major_dimension,
        }

        response = self.do_request('post', 'spreadsheets.values.append', resource_args=resource_args, params=params, json_data=json_data)

        return response
