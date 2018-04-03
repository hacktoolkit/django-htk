# Python Standard Library Imports
import datetime
import time

# Third Party / PIP Imports
import requests
import rollbar

# Django Imports

# HTK Imports
from htk.lib.zuora.constants import *
from htk.utils import htk_setting

class HtkZuoraAPI(object):
    def __init__(self, client_id=None, client_secret=None):
        if client_id is None:
            client_id = htk_setting('HTK_ZUORA_CLIENT_ID')
        if client_secret is None:
            client_secret = htk_setting('HTK_ZUORA_CLIENT_SECRET')

        self.client_id = client_id
        self.client_secret = client_secret

        self.access_token = None
        self.expires_at = None

        zuora_country = htk_setting('HTK_ZUORA_COUNTRY')
        zuora_api_mode = 'prod' if htk_setting('HTK_ZUORA_PROD') else 'sandbox'
        self.api_base_url = HTK_ZUORA_API_BASE_URLS[zuora_country][zuora_api_mode]

        self.authenticate()

    def _get_request_headers(self, headers=None):
        if headers is None:
            headers = {}
        if self.is_authenticated():
            headers.update({
                'Authorization' : 'Bearer %s' % self.access_token,
            })
        else:
            pass
        return headers

    def authenticate(self):
        resource_path = 'oauth/token'
        headers = {
            'Content-Type' : 'application/x-www-form-urlencoded',
        }
        data = {
            'client_id' : self.client_id,
            'client_secret' : self.client_secret,
            'grant_type' : 'client_credentials',
        }
        response = self.do_request('post', resource_path, headers=headers, data=data)
        result = response.json()
        access_token = result.get('access_token', None)
        token_type = result.get('token_type', None)
        expires_in = result.get('expires_in', 0)
        if expires_in:
            # expire 2 minutes earlier to provide a margin of safety
            expires_in = expires_in - 120 if expires_in >= 120 else 0
            self.expires_at = time.time() + expires_in
        self.access_token = access_token

    def is_authenticated(self):
        if self.access_token and self.expires_at:
            if time.time() < self.expires_at:
                status = True
            else:
                self.access_token = None
                self.expires_at = None
                status = False
        else:
            status = False
        return status

    def do_request(self, method, resource_path, headers=None, params=None, data=None, json_data=None, *args, **kwargs):
        method = method.lower()
        action = getattr(requests, method, None)
        if action is None:
            raise Exception('Invalid request method specified: %s' % method)

        params = params if params else {}
        headers = self._get_request_headers(headers=headers)

        url = '%s%s' % (self.api_base_url, resource_path)
        response = action(url, params=params, headers=headers, data=data, json=json_data, *args, **kwargs)
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

    def create_account(self, json_data):
        resource_path = 'v1/accounts'
        response = self.do_request('post', resource_path, json_data=json_data)
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
        json_data = {
            'remove' : [_format_remove(plan_id) for plan_id in remove_plans],
            'add' : [_format_add(plan_id) for plan_id in add_plans],
        }
        response = self.do_request('put', resource_path, json_data=json_data)
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

        json_data = {
            'cancellationPolicy' : cancellation_policy,
            'cancellationEffectiveDate' : cancellation_date,
        }
        response = self.do_request('put', resource_path, json_data=json_data)
        result = response.json()
        return result

    ##
    # Notifications

    def get_notifications(self):
        # TODO: implemented correctly, but somehow not returning data
        resource_path = '/notifications/notification-definitions'
        response = self.do_request('get', resource_path)
        result = response.json()
        return result

