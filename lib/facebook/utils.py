# Third Party (PyPI) Imports
import requests

# HTK Imports
from htk.utils import htk_setting


def get_long_lived_user_access_token(graph_api_version='v10.0'):
    """Get a long-lived User access token generated from a short-lived User access token

    https://developers.facebook.com/docs/facebook-login/access-tokens/refreshing#get-a-long-lived-user-access-token
    """
    url  = 'https://graph.facebook.com/{}/oauth/access_token'.format(graph_api_version)

    client_id = htk_setting('HTK_FACEBOOK_GRAPH_API_APP_ID')
    client_secret = htk_setting('HTK_FACEBOOK_GRAPH_API_APP_SECRET')
    access_token = htk_setting('HTK_FACEBOOK_GRAPH_API_USER_ACCESS_TOKEN')

    params = {
        'grant_type': 'fb_exchange_token',
        'client_id': client_id,
        'client_secret': client_secret,
        'fb_exchange_token': access_token,
    }
    response = requests.get(url, params=params)

    response_json = response.json()
    return response_json
