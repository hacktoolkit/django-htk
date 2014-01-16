from htk.constants.defaults import *
from htk.utils import htk_setting

def get_cache_key_prefix():
    prefix = htk_setting('HTK_CACHE_KEY_PREFIX')
    return prefix
