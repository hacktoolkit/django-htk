# Python Standard Library Imports
import datetime

# Third Party / PIP Imports
import requests
import rollbar

# Django Imports

# HTK Imports
from htk.lib.zuora.constants import *
from htk.utils import htk_setting

class HtkZuoraAPI(object):
    def __init__(self, username=None, password=None):
        if username is None:
            username = htk_setting('HTK_ZUORA_USERNAME')
        if password is None:
            password = htk_setting('HTK_ZUORA_PASSWORD')

        self.username = username
        self.password = password

        zuora_country = htk_setting('HTK_ZUORA_COUNTRY')
        zuora_api_mode = 'prod' if htk_setting('HTK_ZUORA_PROD') else 'sandbox'
        self.api_base_url = HTK_ZUORA_API_BASE_URLS[zuora_country][zuora_api_mode]

    def _get_request_headers(self):
        headers = {
            'apiAccessKeyId' : self.username,
            'apiSecretAccessKey' : self.password,
        }
        return headers

    def do_request(self, method, resource_path, params=None, payload=None, *args, **kwargs):
        method = method.lower()
        action = getattr(requests, method, None)
        if action is None:
            raise Exception('Invalid request method specified: %s' % method)

        params = params if params else {}
        headers = self._get_request_headers()

        url = '%s%s' % (self.api_base_url, resource_path)
        response = action(url, params=params, headers=headers, json=payload, *args, **kwargs)
        return response

    ##
    # Products

    def get_products(self):
        resource_path = 'v1/catalog/products'
        response = self.do_request('get', resource_path)
        result = response.json()
        if result.get('success'):
            products = result.get('products', [])
        else:
            products = []
        return products

    ##
    # Customers

    def create_account(self, payload):
        resource_path = 'v1/accounts'
        response = self.do_request('post', resource_path, payload=payload)
        result = response.json()
        return result

    ##
    # Subscriptions

    def get_subscription(self, subscription_number):
        """Get subscription

        https://www.zuora.com/developer/api-reference/#operation/Object_GETSubscription
        """
        resource_path = 'v1/subscriptions/%s' % subscription_number
        response = self.do_request('get', resource_path)
        subscription = response.json()
        return subscription

    def update_subscription(self, subscription_number, remove_plans=None, add_plans=None):
        """Updates a subscription

        https://www.zuora.com/developer/api-reference/#operation/PUT_Subscription
        """
        resource_path = 'v1/subscriptions/%s' % subscription_number
        today = datetime.date.today().strftime('%Y-%m-%d')

        def _format_add(plan_id):
            return {
                'productRatePlanId' : plan_id,
                'contractEffectiveDate' : today,
            }
        def _format_remove(plan_id):
            return {
                'ratePlanId' : plan_id,
                'contractEffectiveDate' : today,
            }
        payload = {
            'remove' : [_format_remove(plan_id) for plan_id in remove_plans],
            'add' : [_format_add(plan_id) for plan_id in add_plans],
        }
        response = self.do_request('put', resource_path, payload=payload)
        result = response.json()
        return result

    def cancel_subscription(self, subscription_number, cancellation_policy=None, cancellation_date=None):
        """Cancels a subscription

        `cancellation_policy` can be `EndOfCurrentTerm`, `EndOfLastInvoicePeriod`, `SpecificDate`

        https://www.zuora.com/developer/api-reference/#operation/PUT_CancelSubscription
        """
        resource_path = 'v1/subscriptions/%s/cancel' % subscription_number
        if cancellation_date:
            cancellation_policy = 'SpecificDate'
        if cancellation_policy is None:
            cancellation_policy = 'EndOfCurrentTerm'

        payload = {
            'cancellationPolicy' : cancellation_policy,
            'cancellationEffectiveDate' : cancellation_date,
        }
        response = self.do_request('put', resource_path, payload=payload)
        result = response.json()
        return result
