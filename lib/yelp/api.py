import requests

from htk.utils import htk_setting

class YelpAPI(object):
    def __init__(self, api_key=None):
        if api_key is None:
            api_key = htk_setting('HTK_YELP_API_KEY')
        self.api_key = api_key

    def business_lookup(self, business_id):
        """Get detailed business content
        https://www.yelp.com/developers/documentation/v3/business
        """
        base_url = 'https://api.yelp.com/v3/businesses/%(business_id)s'
        url = base_url % {
            'business_id' : business_id,
        }
        headers = {
            'Authorization' : 'Bearer %s' % self.api_key,
        }
        response = requests.get(url, headers=headers)
        data = response.json()
        return data
