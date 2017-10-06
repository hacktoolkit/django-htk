# Zillow API
# http://www.zillow.com/howto/api/APIOverview.htm

from bs4 import BeautifulSoup
import requests
import rollbar

from htk.utils import htk_setting

def parse_zestimate_response(response):
    soup = BeautifulSoup(response.content, 'xml')
    zresponse = soup.response
    zestimate = {
        'zpid' : zresponse.zpid.string,
        'url' : zresponse.links.homedetails.string,
        'address' : {
            'street' : zresponse.address.street.string,
            'zipcode' : zresponse.address.zipcode.string,
            'city' : zresponse.address.city.string,
            'state' : zresponse.address.state.string,
            'latitude' : zresponse.address.latitude.string,
            'longitude' : zresponse.address.longitude.string,
        },
        'zestimate' : {
            'amount' : zresponse.zestimate.amount.string,
            'last_updated' : zresponse.zestimate.find('last-updated').string,
            'value_change' : zresponse.zestimate.valueChange.string or 0,
            'low' : zresponse.zestimate.valuationRange.low.string or 0,
            'high' : zresponse.zestimate.valuationRange.high.string or 0,
        },
    }
    return zestimate

def get_zestimate(zpid, zwsid=None):
    """Get the Zestimate for `zpid`
    `zpid` Zillow property id

    http://www.zillow.com/howto/api/GetZestimate.htm
    """
    if zwsid is None:
        zwsid = htk_setting('HTK_ZILLOW_ZWSID')

    url = 'http://www.zillow.com/webservice/GetZestimate.htm'
    params = {
        'zws-id' : zwsid,
        'zpid' : zpid,
    }
    response = requests.get(url, params=params)
    if response.status_code == 200:
        try:
            zestimate = parse_zestimate_response(response)
        except:
            zestimate = None
            extra_data = {
                'url' : url,
                'params' : params,
            }
            rollbar.report_exc_info(extra_data=extra_data)
    else:
        zestimate = None
    return zestimate
