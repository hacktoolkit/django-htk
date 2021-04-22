# Third Party (PyPI) Imports
import requests
import rollbar

# HTK Imports
from htk.lib.airtable.exceptions import AirtableNoBaseConfigured


class AirtableAPI:
    """Airtable API

    API Docs: https://airtable.com/{baseId}/api/docs
    """
    def __init__(self, base_id, api_key_ro=None, api_key_rw=None):
        if base_id is None:
            raise AirtableNoBaseConfigured

        self.base_id = base_id
        self.api_key_ro = api_key_ro
        self.api_key_rw = api_key_rw

    def get_records(self, table, view_name, limit=100, page_size=100):
        headers = {
            'Authorization': 'Bearer {}'.format(self.api_key_ro),
        }

        params = {
            'view': view_name,
            'maxRecords': limit,
            'pageSize': page_size,
        }

        url = 'https://api.airtable.com/v0/{base_id}/{table}'.format(
            base_id=self.base_id,
            table=table
        )

        # TODO: handle pagination, 429
        response = requests.get(url, headers=headers, params=params)

        response_json = response.json()
        if 'records' in response_json:
            records = response_json['records']
        else:
            records = []

            extra_data = {
                'base_id': self.base_id,
                'table': table,
                'view_name': view_name,
                'url': url,
                'params': params,
                'response': response_json,
            }
            rollbar.report_message('Airtable API error: No records matching query', extra_data=extra_data)

        return records
