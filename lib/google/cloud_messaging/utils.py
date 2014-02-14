from gcm.gcm import GCM

from htk.utils import htk_setting

def get_gcm_client():
    gcm_api_key = htk_setting('HTK_GCM_API_KEY', None)
    if gcm_api_key:
        client = GCM(gcm_api_key)
    else:
        # TODO: raise exception?
        client = None
    return client
