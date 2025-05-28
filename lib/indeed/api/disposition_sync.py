# Third Party (PyPI) Imports
import rollbar

# HTK Imports
from htk.api.auth import HTTPBearerAuth
from htk.lib.indeed.api.base import IndeedBaseSyncAPI
from htk.lib.indeed.constants import INDEED_GRAPHQL_API_URL


class IndeedDispositionSyncAPI(IndeedBaseSyncAPI):
    """API to post the disposition status of applications received through Indeed

    Indeed uses GraphQL API to update disposition status of applications
    Ref: https://docs.indeed.com/disposition-sync-api/
    """

    def __init__(self, client_id, client_secret, dispositions):
        super().__init__(client_id, client_secret)
        self.dispositions = dispositions

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
            INDEED_GRAPHQL_API_URL,
            auth=auth,
            json={'query': mutation, 'variables': variables},
        )
        total_good_dispositions, failed_dispositions = self.handle_response(
            response_json, status_code
        )

        return total_good_dispositions, failed_dispositions
