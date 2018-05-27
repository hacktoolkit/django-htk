from htk.lib.iterable.api import HtkIterableAPIClient
from htk.utils import htk_setting

def get_iterable_api_client():
    """Returns an initialized Iterable API client
    """
    api_key = htk_setting('HTK_ITERABLE_API_KEY')
    itbl = HtkIterableAPIClient(api_key)
    return itbl

def get_campaign_id(key):
    """Get a campaign id by `key`
    """
    campaign_ids = htk_setting('HTK_ITERABLE_CAMPAIGN_IDS')
    campaign_id = campaign_ids.get(key)
    return campaign_id

def get_list_id(key):
    """Get a list id by `key`
    """
    list_ids = htk_setting('HTK_ITERABLE_LIST_IDS')
    list_id = list_ids.get(key)
    return list_id

def get_workflow_id(key):
    """Get a workflow id by `key`
    """
    workflow_ids = htk_setting('HTK_ITERABLE_WORKFLOW_IDS')
    workflow_id = workflow_ids.get(key)
    return workflow_id
