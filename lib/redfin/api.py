import json
import requests

from htk.lib.redfin.constants import *

class RedfinAPI(object):
    def __init__(self):
        pass

    def _get_api_request(self, endpoint_name, params):
        url = '%s%s' % (REDFIN_API_BASE_URL, self._get_api_endpoint_url(endpoint_name),)

        referrer_base_url = 'https://www.redfin.com/what-is-my-home-worth'
        referrer_params = {
            k : v
            for k, v in params.iteritems()
            if k in ['propertyId', 'listingId',]
        }
        referrer_url = requests.PreparedRequest().prepare_url(referrer_base_url, referrer_params)

        headers = {
            'Accept' : '*/*',
            #'Accept' : 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Encoding' : 'gzip, deflate, br',
            'Accept-Language' : 'en-US,en;q=0.9',
            'Cache-Control' : 'no-cache',
            'Connection' : 'keep-alive',
            'Content-Type' : 'application/json',
            'Host' : 'www.redfin.com',
            'Pragma' : 'no-cache',
            'Upgrade-Insecure-Requests' : '1',
            'Referer' : referrer_url,
            'User-Agent' : 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.140 Safari/537.36',
        }

        cookies = {
            'RF_BROWSER_ID' : '',
            'RF_ACCESS_LEVEL' : '',
            'RF_AUTH' : '',
            'RF_LAST_ACCESS' : '',
            'RF_SECURE_AUTH' : '',
            'RF_W_AUTH' : '',
        }

        response = requests.get(url, params=params, headers=headers, cookies=cookies, timeout=3)
        #print response.text
        return response

    def _get_api_endpoint_url(self, endpoint_name):
        url = REDFIN_API_ENDPOINTS.get(endpoint_name)
        return url

    def get_home_worth(self, property_id):
        """https://www.redfin.com/what-is-my-home-worth?propertyId={property_id}&listingId={listing_id}
        """
        pass

    def get_property_listing_id(self, property_id):
        """Get property listing id
        https://www.redfin.com/stingray/do/api-get-property-listing-id?propertyId={property_id}

        Response:
        {}&&{"resultCode":0,"errorMessage":"Success","version":156,"payload":{"listingId":"123456789"}}
        """
        params = {
            'propertyId' : property_id,
        }
        response = self._get_api_request('get_property_listing_id', params)
        if response.status_code == 200:
            response_json = json.loads(response.text[4:])
            listing_id = response_json.get('payload', {}).get('listingId', None)
        else:
            listing_id = None
        return listing_id

    def get_avm(self, property_id, listing_id=None):
        """Get AVM for `property_id`

        AVM = Automated Valuation Model

        https://www.redfin.com/stingray/api/home/details/avm?propertyId={property_id}&listingId={listing_id}&accessLevel=3

        Response:
        {}&&{"errorMessage":"Success","resultCode":0,"payload":{"displayLevel":1,"propertyId":1234567,"predictedValue":1234567.00,"predictedValueHistorical":1234567.00,"lastSoldPrice":123456,"lastSoldDate":1234567800000,"listingTimezone":"US/Pacific","numBeds":10,"numBaths":12.0,"sqFt":{"value":12000},"comparables":[],"isServiced":true,"isActivish":false,"showInHeader":true,"isHidden":false,"isVisibilityRestricted":false,"soldDate":1234567800000,"soldDateTimeZone":"US/Pacific","latLong":{"latitude":37.00,"longitude":-121.00},"priceInfo":{"amount":1234567,"label":"Sold Jan 30, 2017","displayLevel":1},"searchStatusId":4,"streetAddress":{"streetNumber":"12345","directionalPrefix":"","streetName":"MAIN","streetType":"St","directionalSuffix":"","unitType":"","unitValue":"","addressDisplayLevel":{"displayLevel":1,"displayText":""},"assembledAddress":"12345 MAIN St","includeStreetNumber":true},"sectionPreviewText":"$1,234,567 (+$123k since last sold)"},"version":156}
        """
        if listing_id is None:
            listing_id = self.get_property_listing_id(property_id)
        params = {
            'propertyId' : property_id,
            'listingId' : listing_id,
            'accessLevel' : 1,
        }
        response = self._get_api_request('get_avm', params)
        if response.status_code == 200:
            response_json = json.loads(response.text[4:])
            data = response_json
        else:
            data = {}
        return data

    def get_property_parcel_info(self, property_id, listing_id=None):
        """Get Property Parcel Info
        https://www.redfin.com/stingray/api/home/details/propertyParcelInfo?propertyId=1474895&listingId=37807759&accessLevel=3

        Response:
        {}&&{"errorMessage":"Success","resultCode":0,"payload":{"staticMapUrl":"https://maps.google.com/maps/api/staticmap?...,"staticMapUrl2x":"https://maps.google.com/maps/api/staticmap?...","bounds":[{"lat":"","long":""},{"lat":"","long":""},{"lat":"","long":""},{"lat":"","long":""},{"lat":"","long":""}],"mapLocationDisplayLevel":1,"sectionPreviewText":"Map and directions"},"version":156}
        """

        if listing_id is None:
            listing_id = self.get_property_listing_id(property_id)
        params = {
            'propertyId' : property_id,
            'listingId' : listing_id,
            'accessLevel' : 1,
        }
        response = self._get_api_request('get_property_parcel_info', params)
        if response.status_code == 200:
            response_json = json.loads(response.text[4:])
            data = response_json
        else:
            data = None
        return data
