# eGauge XML API
# https://www.egauge.net/docs/egauge-xml-api.pdf
#
# Examples: https://teslamotorsclub.com/tmc/threads/egauge-3-system-review-energy-monitoring.57844/

from bs4 import BeautifulSoup
import datetime
import requests
import time

from htk.utils.datetime_utils import tznow

class EgaugeAPI(object):
    def __init__(self, name, *args, **kwargs):
        self.name = name

    def get_url(self, api_type):
        from htk.lib.egauge.constants import EGAUGE_API_URLS
        url = EGAUGE_API_URLS[api_type] % self.name
        return url

    def _parse_instantaneous_data_xml_response(self, response):
        """
        <?xml version="1.0" encoding="UTF-8" ?>
        <data serial="0x40cf5ba7">
          <ts>1485929958</ts>
          <r t="P" n="Solar"><v>468321586</v></r>
          <r t="P" n="Solar+"><v>469782890</v></r>
          <r t="P" n="Pool Subpanel"><v>477858627</v></r>
          <r t="P" n="Subpanel "><v>7845162</v></r>
          <r t="P" n="Test CT1"><v>510651636</v></r>
          <r t="P" n="Test CT2"><v>-501585489</v></r>
          <r t="P" n="Test CT3"><v>238673736</v></r>
        </data>
        """
        #print '\n'.join([response.url, response.status_code, response.content,])
        soup = BeautifulSoup(response.content, 'xml')
        egauge_response = soup.response
        data = {
            'ts' : int(soup.find('ts').string),
            'values' : {
                r.attrs.get('n') : int(r.string,)
                for r in soup.find_all('r')
            },
        }
        return data

    def get_instantaneous_data(self):
        url = self.get_url('instantaneous')
        params = {
            #'tot' : None,
            #'teamstat' : None,
            #'inst' : None,
        }
        response = requests.get(url, params=params)
        egauge_data = self._parse_instantaneous_data_xml_response(response)
        return egauge_data

    def _parse_stored_data_xml_response(self, response):
        """
        <?xml version="1.0" encoding="UTF-8" ?>
        <!DOCTYPE group PUBLIC "-//ESL/DTD eGauge 1.0//EN" "http://www.egauge.net/DTD/egauge-hist.dtd">
        <group serial="0x40cf5ba7">
          <data columns="7" time_stamp="0x58917ce4" time_delta="86400" epoch="0x587fd9a8">
            <cname t="P">Solar</cname>
            <cname t="P">Solar+</cname>
            <cname t="P">Pool Subpanel</cname>
            <cname t="P">Subpanel </cname>
            <cname t="P">Test CT1</cname>
            <cname t="P">Test CT2</cname>
            <cname t="P">Test CT3</cname>
            <r><c>468321451</c><c>469782746</c><c>477817721</c><c>7844266</c><c>510490316</c><c>-501425065</c><c>238653420</c></r>
            <r><c>426467404</c><c>427926214</c><c>439663841</c><c>7180751</c><c>473753254</c><c>-465351518</c><c>219603582</c></r>
          </data>
        </group>
        """
        #print '\n'.join([response.url, str(response.status_code), response.content,])
        soup = BeautifulSoup(response.content, 'xml')
        egauge_response = soup.response
        data = {
            'column_names' : [cname.string for cname in soup.find_all('cname')],
            'values' : [
                [int(col.string) for col in row.find_all('c')]
                for row in soup.find_all('r')
            ],
        }
        return data

    def get_stored_data(self, q_params=None):
        if q_params is None:
            q_params = [
                'a',
                'E',
                'C',
                'd',
            ]
        q_string = '' if not len(q_params) else '?%s' % '&'.join(q_params)
        url = self.get_url('stored') + q_string
        params = {
            # TODO: specify param without value in dict
            # https://github.com/kennethreitz/requests/issues/2651
            #'a' : '', # return virtual and remote headers
            #'E' : '', # Requests that values are output relative to epoch
            #'C' : '', # Specifies that the returned data be delta-compressed. That is, after the first row of data, each subsequent row's columns are expressed as a difference relative to the previous row's column-values.
            #'m' : '', # minutes
            #'h' : '', # hours
            #'d' : '', # days
            #'S' : None, # seconds
            'n' : 3, # max number of rows to be returned
            #'f' : time.mktime(tznow().timetuple()),
            #'w' : int(time.mktime((tznow() - datetime.timedelta(hours=24)).timetuple())),
        }
        response = requests.get(url, params=params)
        egauge_data = self._parse_stored_data_xml_response(response)
        return egauge_data
