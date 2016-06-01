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
        url = self.get_resource_url(resource_type)
        headers = {
            'X-FullContact-APIKey' : self.api_key,
        }
        response = requests.get(url, headers=headers, params=params)
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
                print person
            except:
                pass
        else:
            pass
        return person

class FullContactObject(object):
    pass

class FullContactPerson(FullContactObject):
    def __init__(self, person_data):
        self.data = person_data
