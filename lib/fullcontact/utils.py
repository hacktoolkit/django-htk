import random

from htk.lib.fullcontact.classes import FullContactAPI
from htk.utils import htk_setting

def get_full_contact_api_key():
    """Retrieves a FullContact API key
    """
    api_keys = htk_setting('HTK_FULLCONTACT_API_KEYS')
    api_key = random.choice(api_keys)
    return api_key

def get_full_contact_api():
    api_key = get_full_contact_api_key()
    api = FullContactAPI(api_key)
    return api

def find_person_by_email(email):
    api = get_full_contact_api()
    person = api.get_person(email)
    return person
