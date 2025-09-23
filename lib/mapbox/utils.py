# HTK Imports
from htk.utils import htk_setting


def get_access_token(backend=True):
    key = (
        'HTK_MAPBOX_ACCESS_TOKEN'
        if backend
        else 'HTK_MAPBOX_ACCESS_TOKEN_FRONTEND'
    )
    access_token = htk_setting(key)
    return access_token


def get_access_token_frontend():
    return get_access_token(backend=False)
