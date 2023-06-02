# Third Party (PyPI) Imports
import requests
import rollbar
from six.moves import urllib

# HTK Imports
from htk.utils.request import get_current_request


ZIPRECRUITER_ENTRY_POINT_URL = 'https://api.ziprecruiter.com/partner/v0/job/'


class ZipRecruiterAPI(object):
    """The Job API is used to create/update/delete jobs in ZipRecruiter

    https://www.ziprecruiter.com/partner/documentation/#job-api
    """
    def __init__(self, api_key):
        self.api_key = api_key

    def build_request_url(self, resource_path=None):
        request_url = urllib.parse.urljoin(ZIPRECRUITER_ENTRY_POINT_URL, resource_path)
        return request_url

    def build_request_headers(self):
        """Creates a header to pass in for GET/POST/PUT/DELETE request

        More about the authorization header can be found here:
        https://www.ziprecruiter.com/partner/documentation/#authentication
        """
        headers = {
            'Authorization': 'Basic {}'.format(self.api_key),
            'Content-Type': 'application/json',
        }
        return headers

    def handle_bad_response(self, response=None, error_msg=None):
        request = get_current_request()
        if response is not None:
            api_request = response.request

            extra_data = {
                'api_request': {
                    'url': api_request.url,
                    'method': api_request.method,
                    'body': api_request.body,
                },
                'response': {
                    'status_code': response.status_code,
                    'text': response.text,
                },
            }
        else:
            extra_data = {}

        if error_msg:
            extra_data.update({
                'message': '{}'.format(error_msg),
            })
        else:
            pass

        rollbar.report_message(
            'ZipRecruiter Job API Bad Response',
            request=request,
            extra_data=extra_data
        )

    def do_request(self, method, resource_path=None, json_data=None, *args, **kwargs):
        method = method.lower()
        action = getattr(requests, method, None)
        if action is None:
            raise Exception('Invalid request method specified: %s' % method)

        headers = self.build_request_headers()
        url = self.build_request_url(resource_path)

        response = None
        try:
            response = action(url, headers=headers, json=json_data, *args, **kwargs)
            response_json = response.json()
        except Exception as e:
            response_json = None
            self.handle_bad_response(response=response, error_msg=e)

        return response_json
