# Python Standard Library Imports
import json

# Third Party (PyPI) Imports
import requests
from requests_oauthlib import OAuth1

# Django Imports
from django.conf import settings

# HTK Imports
from htk.lib.linkedin.constants import *


def get_profile_data(resource_owner_key, resource_owner_secret):
    oauth = OAuth1(
        settings.SOCIAL_AUTH_LINKEDIN_KEY,
        client_secret=settings.SOCIAL_AUTH_LINKEDIN_SECRET,
        resource_owner_key=resource_owner_key,
        resource_owner_secret=resource_owner_secret
    )

    linkedin_api_endpoint = LINKEDIN_PROFILE_API_BASE_URL % ','.join(LINKEDIN_PROFILE_FIELDS)
    response = requests.get(
        url=linkedin_api_endpoint,
        auth=oauth
    )
    # TODO: uncomment to purposely raise Exception and see format
    #raise Exception(response.text)
    linkedin_profile_data = json.loads(response.text)
    return linkedin_profile_data
