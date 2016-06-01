import requests

from htk.lib.fullcontact.constants import *

class FullContactAPI(object):
    """
    https://www.fullcontact.com/developer/docs/
    """
    def __init__(self, api_key):
        self.api_key = api_key

    def get_resource_url(self, resource_type):
        """Returns the resource URL for `resource_type`
        """
        url = '%s%s' % (
            FULLCONTACT_API_BASE_URL,
            FULLCONTACT_API_RESOURCES.get(resource_type),
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
                person = FullContactPerson(data)
            except:
                pass
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
            for email, request_url in email_api_request_urls.iteritems():
                if request_url in responses:
                    person_response = responses[request_url]
                    if person_response['status'] == 200:
                        persons[email] = person_response
        else:
            pass
        return persons

class FullContactObject(object):
    pass

class FullContactPerson(FullContactObject):
    def __init__(self, person_data):
        self.data = person_data
