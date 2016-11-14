import requests

from htk.lib.google.gmail.constants import GMAIL_RESOURCES

# https://developers.google.com/gmail/api/v1/reference/

def get_resource_url(resource_name, email):
    url = GMAIL_RESOURCES[resource_name] % email
    return url

def get_authorization_header(user, email):
    g_auth_data = user.profile.get_social_user('google-oauth2', email)
    header = None
    if g_auth_data:
        header = '%(token_type)s %(access_token)s' % g_auth_data.extra_data
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
