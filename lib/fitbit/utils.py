from htk.lib.fitbit.api import FitbitAPI

def get_fitbit_api_django(social_auth_user):
    from django.conf import settings
    client_id = settings.SOCIAL_AUTH_FITBIT_KEY
    client_secret = settings.SOCIAL_AUTH_FITBIT_SECRET
    api = get_fitbit_api(social_auth_user, client_id, client_secret)
    return api

def get_fitbit_api(social_auth_user, client_id, client_secret):
    api = FitbitAPI(social_auth_user, client_id, client_secret)
    return api

def get_fitbit_social_auth_user(user):
    from htk.apps.accounts.utils.social_utils import get_social_auth_for_user
    social_auth_user = get_social_auth_for_user(user, 'fitbit')
    return social_auth_user

def get_devices_for_user(user, social_auth_user=None):
    if social_auth_user is None:
        social_auth_user = get_fitbit_social_auth_user(user)
    api = get_fitbit_api_django(social_auth_user)
    devices = api.get_devices()
    return devices
