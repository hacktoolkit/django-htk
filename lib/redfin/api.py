# Python Standard Library Imports
import json

# Third Party / PIP Imports
import requests
import rollbar

# HTK Imports
from htk.lib.redfin.constants import *
from htk.utils.urls import build_url_with_query_params


class RedfinAPI(object):
    def __init__(self):
        pass

    def _get_api_request(self, endpoint_name, params):
        url = '%s%s' % (REDFIN_API_BASE_URL, self._get_api_endpoint_url(endpoint_name),)

        referrer_url = self.get_home_worth_url(params.get('propertyId'), params.get('listingId'))

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

    def get_home_worth_url(self, property_id, listing_id=None):
        """https://www.redfin.com/what-is-my-home-worth?propertyId={property_id}&listingId={listing_id}
        """
        base_url = 'https://www.redfin.com/what-is-my-home-worth'
        params = {
            'propertyId' : property_id,
            'listingId' : listing_id,
        }
        url = build_url_with_query_params(base_url, params)
        r = requests.PreparedRequest()
        r.prepare_url(base_url, params)
        return r.url

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
            avm_data = response_json.get('payload', None)
            if avm_data is None:
                extra_data = {
                    'property_id' : property_id,
                    'listing_id' : listing_id,
                }
                rollbar.report_message('Redfin API Missing AVM Payload', 'info', extra_data=extra_data)
                avm_data = {}
        else:
            avm_data = {}

        home_worth_url = self.get_home_worth_url(property_id, listing_id=listing_id)
        avm = RedfinAVM(property_id, home_worth_url, avm_data)
        return avm

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

class RedfinAVM(object):
    def __init__(self, property_id, home_worth_url, raw_data):
        self.property_id = property_id
        self.home_worth_url = home_worth_url
        self.raw_data = raw_data

        self.property_value = raw_data.get('predictedValue', 0)
        self.property_value_historical = raw_data.get('predictedValueHistorical', 0)
        if self.property_value_historical != 0:
            self.property_value_change = self.property_value - self.property_value_historical
        else:
            self.property_value_change = self.property_value

        lat_long = raw_data.get('latLong', {})
        if lat_long:
            self.latitude = lat_long.get('latitude')
            self.longitude = lat_long.get('longitude')

        # build the address
        street_address = raw_data.get('streetAddress', {}).get('assembledAddress', None)

        if street_address:
            self.street_address = street_address
            # full address is not directly returned
            # assume the first comparable is in same city, state, zip
            # alternatively, could reverse geocode the lat-lng
            comparables = raw_data.get('comparables', [])
            comparable = comparables[0] if len(comparables) > 0 else {}

            self.city = comparable.get('city', 'Unknown City')
            self.state = comparable.get('state', 'Unknown State')
            self.zipcode = comparable.get('zip', '')

            self.address = '%s, %s, %s %s' % (
                street_address,
                self.city,
                self.state,
                self.zipcode,
            )

    def to_json(self):
        """Returns a JSON-encodable dictionary representation of the Redfin AVM `self.property_id`
        """
        data = {
            'property_id' : self.property_id,
            'property_value' : self.property_value,
            'city' : self.city,
            'state' : self.state,
            'zipcode' : self.zipcode,
            'address' : self.address,
        }
        return json
