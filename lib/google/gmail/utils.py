# Python Standard Library Imports
import time

# Third Party / PIP Imports
import requests

# HTK Imports
from htk.lib.google.gmail.constants import GMAIL_RESOURCES

# https://developers.google.com/gmail/api/v1/reference/

def get_resource_url(resource_name, email=None, **kwargs):
    user_id = email if email else 'me'
    values = {
        'user_id' : user_id,
    }
    values.update(kwargs)
    url = GMAIL_RESOURCES[resource_name] % values
    return url

def get_authorization_header(user, email):
    g_social_auth = user.profile.get_social_user('google-oauth2', email)
    header = None
    if g_social_auth:
        # refreshes token if necessary
        from social_django.utils import load_strategy
        access_token = g_social_auth.get_access_token(load_strategy())
        values = {
            'token_type' : g_social_auth.extra_data['token_type'],
            'access_token' : access_token,
        }
        header = '%(token_type)s %(access_token)s' % values
    return header

##
# Users.drafts
# https://developers.google.com/gmail/api/v1/reference/#Users.drafts

##
# Users.history
# https://developers.google.com/gmail/api/v1/reference/#Users.history

##
# User.labels
# https://developers.google.com/gmail/api/v1/reference/#Users.labels

def labels_list(user, email):
    """https://developers.google.com/gmail/api/v1/reference/users/labels/list
    """
    url = get_resource_url('labels_list', email)
    headers = {
        'Authorization' : get_authorization_header(user, email),
    }
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        response_json = response.json()
        labels = response_json['labels']
        labels = sorted(labels, key=lambda label: label['name'])
    elif response.status_code == 401:
        # unauthorized
        labels = None
    else:
        labels = None
    return labels

##
# Users.messages
# https://developers.google.com/gmail/api/v1/reference/#Users.messages

def messages_list(user, email, q=''):
    """https://developers.google.com/gmail/api/v1/reference/users/messages/list
    """
    url = get_resource_url('messages_list', email)
    headers = {
        'Authorization' : get_authorization_header(user, email),
    }
    params = {}
    if q:
        params['q'] = q
    response = requests.get(url, headers=headers, params=params)
    if response.status_code == 200:
        response_json = response.json()
        messages = response_json.get('messages', [])
    elif response.status_code == 401:
        # unauthorized
        messages = []
    else:
        messages = []
    return messages

def message_get(user, email, message_id):
    """https://developers.google.com/gmail/api/v1/reference/users/messages/get
    """
    kwargs = {'message_id' : message_id,}
    url = get_resource_url('message_get', email, **kwargs)
    headers = {
        'Authorization' : get_authorization_header(user, email),
    }
    params = {}
    response = requests.get(url, headers=headers, params=params)
    if response.status_code == 200:
        response_json = response.json()
        message = response_json
    elif response.status_code == 401:
        # unauthorized
        message = None
    else:
        message = None
    return message

##
# Users.messages.attachments
# https://developers.google.com/gmail/api/v1/reference/#Users.messages.attachments

##
# Users.threads
# https://developers.google.com/gmail/api/v1/reference/#Users.threads

##
# Users.settings
# https://developers.google.com/gmail/api/v1/reference/#Users.settings

##
# Users.settings.forwardingAddresses
# https://developers.google.com/gmail/api/v1/reference/#Users.settings.forwardingAddresses

##
# Users
# https://developers.google.com/gmail/api/v1/reference/#Users

##
# Users.settings.filters
# https://developers.google.com/gmail/api/v1/reference/#Users.settings.filters

##
# Users.settings.sendAs
# https://developers.google.com/gmail/api/v1/reference/#Users.settings.sendAs
