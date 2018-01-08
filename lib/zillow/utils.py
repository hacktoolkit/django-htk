# Zillow API
# http://www.zillow.com/howto/api/APIOverview.htm

from bs4 import BeautifulSoup
import requests
import rollbar

from htk.utils import htk_setting

def parse_zestimate_response(response):
    soup = BeautifulSoup(response.content, 'xml')

    zresponse = soup.response
    if zresponse:
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
    else:
        zestimate = None
    return zestimate

class Zestimate(object):
    HOME_DETAILS_BASE_URL = 'https://www.zillow.com/homedetails/%s_zpid'
    ZESTIMATE_URL = 'http://www.zillow.com/webservice/GetZestimate.htm'

    def __init__(self, zpid, zwsid):
        self.zpid = zpid
        self.zwsid = zwsid
        self.home_details_url = Zestimate.HOME_DETAILS_BASE_URL % self.zpid

        self._fetch()
        self._safe_parse()

    def _fetch(self):
        url = Zestimate.ZESTIMATE_URL
        params = {
            'zws-id' : self.zwsid,
            'zpid' : self.zpid,
        }
        try:
            response = requests.get(url, params=params)
            if response.status_code == 200:
                self.xml = response.content
            else:
                self.xml = None
        except:
            self.xml = None
            extra_data = self._rollbar_extra_data()
            extra_data.update({
                'url' : url,
                'params' : params,
            })
            rollbar.report_exc_info(extra_data=extra_data)

    def _safe_parse(self):
        try:
            self._parse()
        except:
            extra_data = self._rollbar_extra_data()
            rollbar.report_exc_info(extra_data=extra_data)

    def _parse(self):
        if self.xml is None:
            return

        soup = BeautifulSoup(self.xml, 'xml')

        zrequest = soup.request
        if zrequest:
            self.request = {
                'zpid' : zrequest.zpid.string,
            }

        zmessage = soup.message
        if zmessage:
            self.message = zmessage.find('text').get_text()
            self.code = zmessage.code.string

        # the main data we want, to extract the actual Zestimate
        zresponse = soup.response
        if zresponse:
            self.response = {
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
        else:
            self.response = None
            if self.message:
                message = self.message
                extra_data = self._rollbar_extra_data()
                extra_data.update({
                    'code' : self.code if self.code else None,
                    #'xml' : self.xml,
                })
                rollbar.report_message(message, 'info', extra_data=extra_data)

    def _rollbar_extra_data(self):
        extra_data = {
            'zpid' : self.zpid,
            'zwsid' : self.zwsid,
        }
        return extra_data

    def to_json(self):
        """Returns a JSON-encodable dictionary representation of the Zestimate for `self.zpid`
        """
        return self.response

def get_zestimate(zpid, zwsid=None):
    """Get the Zestimate for `zpid`
    `zpid` Zillow property id

    http://www.zillow.com/howto/api/GetZestimate.htm
    """
    if zwsid is None:
        zwsid = htk_setting('HTK_ZILLOW_ZWSID')

    zestimate = Zestimate(zpid, zwsid)
    return zestimate
