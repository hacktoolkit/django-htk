# Python Standard Library Imports
import hashlib
import json

# Third Party / PIP Imports
import requests
import rollbar

# HTK Imports
from htk.utils import htk_setting


def get_api_key():
    api_key = htk_setting('HTK_MAILCHIMP_API_KEY')
    return api_key


def get_api_data_center(api_key):
    """Determine the Mailchimp API Data Center for `api_key`

    http://developer.mailchimp.com/documentation/mailchimp/guides/get-started-with-mailchimp-api-3/
    """
    data_center = api_key.split('-')[1]
    return data_center


def get_api_url(resource, api_key):
    """Determine the Mailchimp API Url for `api_key`

    http://developer.mailchimp.com/documentation/mailchimp/guides/get-started-with-mailchimp-api-3/
    """
    BASE_URL = 'https://%(data_center)s.api.mailchimp.com/3.0%(resource)s'
    data = {
        'data_center' : get_api_data_center(api_key),
        'resource' : resource,
    }
    api_url = BASE_URL % data
    return api_url


def api_call(method, resource, payload, api_key=None):
    if api_key is None:
        api_key = get_api_key()

    api_url = get_api_url(resource, api_key)
    auth = requests.auth.HTTPBasicAuth('user', api_key)
    method = method.lower()
    request_fns = {
        'delete' : requests.delete,
        'get' : requests.get,
        'patch' : requests.patch,
        'post' : requests.post,
        'put' : requests.put,
    }
    response = request_fns[method](api_url, auth=auth, json=payload)
    return response


def subscribe_email(list_id, email, subscribed=False):
    resource_data = {
        'list_id' : list_id,
        'subscriber_hash' : hashlib.md5(email.lower().encode()).hexdigest(),
    }
    resource = '/lists/%(list_id)s/members/%(subscriber_hash)s' % resource_data
    status = 'subscribed' if subscribed else 'pending'

    payload = {
        'email_type' : 'html',
        'status' : status,
        'email_address' : email,
    }
    response = api_call('PUT', resource, payload)
    if response.status_code == 200:
        subscribed = True
    else:
        subscribed = False
    return subscribed
