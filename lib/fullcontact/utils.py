import random
import time

from htk.lib.fullcontact.api import FullContactAPI
from htk.utils import chunks
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
    """Retrieve a person object by `email`
    """
    api = get_full_contact_api()
    person = api.get_person(email)
    return person

def find_valid_emails(emails):
    """Returns a subset of `emails` that are valid
    """
    api = get_full_contact_api()
    all_valid_emails = []
    for chunk in chunks(emails, 20):
        persons = api.get_persons(chunk)
        valid_emails = persons.keys()
        all_valid_emails += valid_emails
        time.sleep(1)
    return all_valid_emails
