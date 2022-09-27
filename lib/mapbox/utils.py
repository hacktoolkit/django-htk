# HTK Imports
from htk.utils import htk_setting


def get_access_token():
    access_token = htk_setting('HTK_MAPBOX_ACCESS_TOKEN')
    return access_token
