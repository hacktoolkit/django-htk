import random

from htk.utils import htk_setting

def get_server_api_key():
    """Retrieves the Google Server API key

    If there are multiple keys configured, selects one at random
    """
    key = htk_setting('HTK_GOOGLE_SERVER_API_KEY')
    if type(key) == str:
        key = key
    elif hasattr(key, '__iter__'):
        key = random.choice(key)
    else:
        key = None
    return key
