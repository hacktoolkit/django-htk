# Python Standard Library Imports

# Third Party / PIP Imports
import requests
import rollbar

# HTK Imports
from htk.lib.fullcontact.constants import *
from htk.utils import htk_setting
from htk.utils import resolve_method_dynamically


class FullContactAPIV3(object):
    """
    https://www.fullcontact.com/developer/docs/
    """
    def __init__(self, api_key):
        self.api_key = api_key

    def get_resource_url(self, resource_type):
        """Returns the resource URL for `resource_type`
        """
        url = '%s%s' % (
            FULLCONTACT_API_V3_BASE_URL,
            FULLCONTACT_API_V3_RESOURCES.get(resource_type),
        )
        return url

    def post(self, resource_type, json_data):
        """Performs a FullContact API POST request
        """
        url = self.get_resource_url(resource_type)
        headers = {
            'Authorization' : 'Bearer {}'.format(self.api_key),
            'Content-Type' : 'application/json',
        }
        response = requests.post(url, headers=headers, json=json_data)
        return response

    def get_person(self, email):
        """
        https://www.fullcontact.com/developer/docs/person/
        """
        person = None
        json_data = {
            'email' : email,
        }
        response = self.post('person', json_data)

        try:
            response_json = response.json()
            if response.status_code == 200:
                person_data = response_json
                FullContactPerson = resolve_method_dynamically(htk_setting('HTK_FULLCONTACT_PERSON_CLASS'))
                person = FullContactPerson(email, person_data, version='v3')
            elif response.status_code == 404:
                # profile not found, do nothing
                pass
            elif response.status_code == 403 and response.message == 'Usage limits for the provided API Key have been exceeded. Please try again later or contact support to increase your limits.':
                extra_data = {
                    'response' : response_json,
                    'redacted_api_key' : '{}...{}'.format(self.api_key[:5], self.api_key[-5:])
                }
                rollbar.report_message('FullContact API key usage limit error', extra_data=
            else:
                # other FullContact API error
                rollbar.report_message('FullContact API error', extra_data={'response' : response_json,})
        except ValueError:
            rollbar.report_exc_info(extra_data={'response' : response,})

        return person

    def get_persons(self, emails):
        """Retrieves a batch of Person objects based on `emails`

        Returns a dictionary mapping emails to Person objects
        """
        rollbar.report_message('Not supported yet in FullContact V3', level='info')
        persons = {}
        return persons


class FullContactAPIV2(object):
    """
    https://www.fullcontact.com/developer/docs/
    """
    def __init__(self, api_key):
        self.api_key = api_key

    def get_resource_url(self, resource_type):
        """Returns the resource URL for `resource_type`
        """
        url = '%s%s' % (
            FULLCONTACT_API_V2_BASE_URL,
            FULLCONTACT_API_V2_RESOURCES.get(resource_type),
        )
        return url

    def get(self, resource_type, params):
        """Performs a FullContact API GET request
        """
        url = self.get_resource_url(resource_type)
        headers = {
            'X-FullContact-APIKey' : self.api_key,
        }
        response = requests.get(url, headers=headers, params=params)
        return response

    def post(self, resource_type, json_payload):
        """Performs a FullContact API POST request
        """
        url = self.get_resource_url(resource_type)
        headers = {
            'X-FullContact-APIKey' : self.api_key,
            'Content-Type' : 'application/json',
        }
        response = requests.post(url, headers=headers, json=json_payload)
        return response

    def batch(self, json_payload):
        response = self.post('batch', json_payload)
        return response

    def get_person(self, email):
        """
        https://www.fullcontact.com/developer/docs/person/
        """
        person = None
        params = {
            'email' : email,
        }
        response = self.get('person', params)
        if response.status_code == 200:
            try:
                data = response.json()
                FullContactPerson = resolve_method_dynamically(htk_setting('HTK_FULLCONTACT_PERSON_CLASS'))
                person = FullContactPerson(email, data, version='v2')
            except:
                rollbar.report_exc_info(extra_data={'response' : response,})
        else:
            pass
        return person

    def get_persons(self, emails):
        """Retrieves a batch of Person objects based on `emails`

        Returns a dictionary mapping emails to Person objects
        """
        person_api_url = self.get_resource_url('person')
        email_api_request_urls = { email : '%s?email=%s' % (person_api_url, email,) for email in emails }
        json_payload = {
            'requests' : email_api_request_urls.values(),
        }
        response = self.batch(json_payload)
        persons = {}
        if response.status_code == 200:
            responses = response.json()['responses']
            for email, request_url in email_api_request_urls.items():
                if request_url in responses:
                    person_data = responses[request_url]
                    if person_data['status'] == 200:
                        FullContactPerson = resolve_method_dynamically(htk_setting('HTK_FULLCONTACT_PERSON_CLASS'))
                        persons[email] = FullContactPerson(email, person_data, version='v2')
        else:
            pass
        return persons
