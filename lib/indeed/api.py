# Python Standard Library Imports
import time

# Third Party (PyPI) Imports
import requests
import rollbar
from requests.auth import HTTPBasicAuth

# HTK Imports
from htk.api.auth import HTTPBearerAuth
from htk.lib.indeed.constants import (
    INDEED_DISPOSITION_AUTH_TOKEN_URL,
    INDEED_DISPOSITION_GRAPHQL_API_URL,
)


class IndeedDispositionSyncAPI(object):
    """API to post the disposition status of applications received through Indeed

    Indeed uses GraphQL API to update disposition status of applications
    Ref: https://docs.indeed.com/disposition-sync-api/
    """

    def __init__(self, client_id, client_secret, dispositions):
        self.client_id = client_id
        self.client_secret = client_secret
        self.dispositions = dispositions
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
            INDEED_DISPOSITION_AUTH_TOKEN_URL,
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
            rollbar._report_message(
                'Indeed disposition sync access token generation failed',
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

    def handle_response(self, response_json, status_code):
        total_good_dispositions = 0
        failed_disposition_ids = []

        if status_code == 200:
            if 'data' in response_json:
                partner_disposition = response_json.get('data').get(
                    'partnerDisposition'
                )
                partner_disposition_sent = partner_disposition.get('send')
                total_good_dispositions = partner_disposition_sent.get(
                    'numberGoodDispositions'
                )
                rollbar.report_message(
                    'Indeed disposition status update succeeded',
                    level='info',
                    extra_data={
                        'total_dispositions_succeeded': total_good_dispositions,
                        'response_json': response_json,
                    },
                )

                failed_dispositions = partner_disposition_sent.get(
                    'failedDispositions'
                )
                if failed_dispositions:
                    failed_disposition_ids = [
                        item['identifiedBy']['indeedApplyID']
                        for item in failed_dispositions
                    ]
                    rollbar.report_message(
                        'Indeed disposition status update failed',
                        extra_data={
                            'failed_dispositions': failed_dispositions,
                            'response_json': response_json,
                        },
                    )
            if 'errors' in response_json:
                rollbar.report_message(
                    'Error updating Indeed disposition status',
                    extra_data={
                        'errors': response_json.get('errors'),
                        'response_json': response_json,
                    },
                )
        else:
            rollbar.report_message(
                'Request to update Indeed disposition status rejected',
                extra_data={
                    'status_code': status_code,
                    'response': response_json,
                },
            )

        return total_good_dispositions, failed_disposition_ids

    def sync(self):
        mutation = """mutation Send($input: SendPartnerDispositionInput!) {
            partnerDisposition {
                send(input: $input) {
                    numberGoodDispositions
                    failedDispositions {
                        identifiedBy {
                            indeedApplyID
                        }
                        rationale
                    }
                }
            }
        }
        """
        variables = {
            'input': {
                "dispositions": self.dispositions,
            }
        }
        access_token = self.get_access_token()
        auth = HTTPBearerAuth(access_token)

        response_json, status_code = self.request_post(
            INDEED_DISPOSITION_GRAPHQL_API_URL,
            auth=auth,
            json={'query': mutation, 'variables': variables},
        )
        total_good_dispositions, failed_dispositions = self.handle_response(
            response_json, status_code
        )

        return total_good_dispositions, failed_dispositions
