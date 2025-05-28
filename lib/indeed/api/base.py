# Python Standard Library Imports
import time

# Third Party (PyPI) Imports
import requests
import rollbar
from requests.auth import HTTPBasicAuth

# HTK Imports
from htk.lib.indeed.constants import INDEED_OAUTH_TOKEN_URL


class IndeedBaseSyncAPI(object):
    def __init__(self, client_id, client_secret):
        self.client_id = client_id
        self.client_secret = client_secret
        self.token_expires_at = 0
        self.access_token = None

    def request_post(self, url, **kwargs):
        response = requests.post(url, **kwargs)
        status_code = response.status_code
        response_json = response.json()

        return response_json, status_code

    def generate_access_token(self):
        """
        Generate access token using app credentials

        Generated token is valid for one hour(3600 seconds)
        Ref: https://docs.indeed.com/getstarted/register-app-and-call-apis#step-5-refresh-your-access-token
        """
        auth = HTTPBasicAuth(self.client_id, self.client_secret)
        headers = {
            'content-type': 'application/x-www-form-urlencoded',
        }
        data = {
            'grant_type': 'client_credentials',
            'scope': 'employer_access',
        }
        response_json, status_code = self.request_post(
            INDEED_OAUTH_TOKEN_URL,
            auth=auth,
            headers=headers,
            data=data,
        )

        if status_code == 200:
            self.access_token = response_json.get('access_token')
            self.token_expires_at = time.time() + int(
                response_json.get('expires_in')
            )
        else:
            self.access_token = None
            self.token_expires_at = None
            rollbar.report_message(
                'Indeed access token generation failed',
                extra_data={
                    'status_code': status_code,
                    'response': response_json,
                },
            )

    def get_access_token(self):
        """
        Returns access token

        Access token is valid for one hour(3600 seconds)
        Re-generate the access token when it expires
        """
        if self.token_expires_at <= time.time():
            self.generate_access_token()
        return self.access_token
