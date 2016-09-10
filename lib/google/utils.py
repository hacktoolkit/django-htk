import random

from htk.utils import htk_setting

def get_num_server_api_keys():
    """Returns the number of Google server API keys configured
    """
    key = htk_setting('HTK_GOOGLE_SERVER_API_KEY')
    if type(key) == str:
        num = 1
    elif hasattr(key, '__iter__'):
        num = len(key)
    else:
        num = 0
    return num

def get_server_api_key(use_pool=False):
    """Retrieves the Google Server API key

    If there are multiple keys configured and `use_pool` is enabled, selects one at random, otherwise the first
    """
    key = htk_setting('HTK_GOOGLE_SERVER_API_KEY')
    if type(key) == str:
        key = key
    elif hasattr(key, '__iter__'):
        if use_pool:
            key = random.choice(key)
        else:
            key = key[0]
    else:
        key = None
    return key
