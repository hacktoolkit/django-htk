from htk.lib.iterable.api import HtkIterableAPIClient
from htk.utils import htk_setting

def get_iterable_api_client():
    """Returns an initialized Iterable API client
    """
    api_key = htk_setting('HTK_ITERABLE_API_KEY')
    itbl = HtkIterableAPIClient(api_key)
    return itbl

def get_workflow_id(key):
    """Get a workflow id by `key`
    """
    workflow_ids = htk_setting('HTK_ITERABLE_WORKFLOW_IDS')
    workflow_id = workflow_ids.get(key)
    return workflow_id
