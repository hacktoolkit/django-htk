def get_fitbit_api(user, social_auth_user=None, client_id=None, client_secret=None):
    from htk.lib.fitbit.api import FitbitAPI

    if client_id is None or client_secret is None:
        # if either is missing, obtain both from Django settings file
        from django.conf import settings
        client_id = settings.SOCIAL_AUTH_FITBIT_KEY
        client_secret = settings.SOCIAL_AUTH_FITBIT_SECRET

    if social_auth_user is None:
        from htk.apps.accounts.utils.social_utils import get_social_auth_for_user
        social_auth_user = get_social_auth_for_user(user, 'fitbit')

    api = FitbitAPI(social_auth_user, client_id, client_secret)
    return api


def get_devices_for_user(user, social_auth_user=None):
    api = get_fitbit_api(user, social_auth_user=social_auth_user)
    devices = api.get_devices()
    return devices


def get_activity_for_user(user, social_auth_user=None):
    api = get_fitbit_api(user, social_auth_user=social_auth_user)
    activity = api.get_activity_steps_past_month()
    return activity
