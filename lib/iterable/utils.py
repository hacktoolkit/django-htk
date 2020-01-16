# HTK Imports
from htk.lib.iterable.api import HtkIterableAPIClient
from htk.utils import find_json_value
from htk.utils import htk_setting


def get_iterable_api_client():
    """Returns an initialized Iterable API client
    """
    api_key = htk_setting('HTK_ITERABLE_API_KEY')
    itbl = HtkIterableAPIClient(api_key)
    return itbl


def list_campaign_keys():
    from htk.utils.json_utils import find_all_json_paths
    campaign_ids = htk_setting('HTK_ITERABLE_CAMPAIGN_IDS')
    keys = find_all_json_paths(campaign_ids)
    return keys


def get_campaign_id(key):
    """Get a campaign id by `key`
    """
    campaign_ids = htk_setting('HTK_ITERABLE_CAMPAIGN_IDS')
    campaign_id = find_json_value(campaign_ids, key)

    return campaign_id


def get_list_id(key):
    """Get a list id by `key`
    """
    list_ids = htk_setting('HTK_ITERABLE_LIST_IDS')
    list_id = find_json_value(list_ids, key)

    return list_id


def get_workflow_id(key):
    """Get a workflow id by `key`
    """
    workflow_ids = htk_setting('HTK_ITERABLE_WORKFLOW_IDS')
    workflow_id = find_json_value(workflow_ids, key)

    return workflow_id
