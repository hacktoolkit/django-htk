# Python Standard Library Imports
import hashlib
import hmac
import time

# Third Party (PyPI) Imports
import requests
import rollbar

# HTK Imports
from htk.lib.dynamic_screening_solutions.constants import *
from htk.utils import (
    htk_setting,
    utcnow,
)
from htk.utils.request import get_current_request


# isort: off


# Python 2 to 3 compatable import
# See: https://python-future.org/compatible_idioms.html#urllib-module
try:
    from urllib.parse import urlparse
except ImportError:
    import urlparse


MAX_RETRY_ATTEMPTS = 5


class Htk321FormsAPI(object):
    """321Forms - Dynamic Screening Solutions

    https://api.321forms.com/docs
    """

    def __init__(self, username=None, secret_key=None, *args, **kwargs):
        self.username = (
            username if username else htk_setting('HTK_321FORMS_USERNAME')
        )
        self.secret_key = (
            secret_key if secret_key else htk_setting('HTK_321FORMS_SECRET')
        )
        self.entry_point_url = htk_setting('HTK_321FORMS_ENTRY_POINT_URL')

    def _get_rollbar_extra_data(self):
        extra_data = {
            'username': self.username,
        }
        return extra_data

    def get_request_url(self, resource_path=None):
        request_url = urlparse.urljoin(self.entry_point_url, resource_path)
        return request_url

    def _make_authorization_key(self, headers, secret_key):
        """Generates the Authorization key signature based on the request `headers`

        Secret key-hashed Base64
        """
        import base64

        base_string = '{"Username":"%s","SentDate":"%s","Action":"%s"}' % (
            headers['Username'],
            headers['SentDate'],
            headers['Action'],
        )
        signature = base64.b64encode(
            hmac.new(
                bytes(secret_key), base_string, digestmod=hashlib.sha1
            ).digest()
        )
        return signature

    def make_request_headers(
        self, action='GET', username=None, secret_key=None
    ):
        """Creates a header to pass in for GET/POST request

        `action`: 'GET' or 'POST'

        More about the authorization header can be found here: https://api.321forms.com/docs
        """
        username = username if username else self.username
        secret_key = secret_key if secret_key else self.secret_key

        sent_date = utcnow().strftime('%Y-%m-%d %H:%M:%S')
        headers = {
            'Username': username,
            'SentDate': "{ts \'%s\'}" % sent_date,
            'Action': action,
        }

        authorization_key = self._make_authorization_key(headers, secret_key)
        headers['Authorization'] = authorization_key
        return headers

    def handle_bad_response(self, response, response_json=None):
        request = get_current_request()
        api_request = response.request

        extra_data = self._get_rollbar_extra_data()
        response_data = {
            'status_code': response.status_code,
        }

        default_message = '321Forms API Bad Response'

        if response_json:
            response_data['json'] = response_json
            error_message = response_json.get('message')
        else:
            response_data['text'] = response.text
            error_message = None

        extra_data.update(
            {
                'api_request': {
                    'url': api_request.url,
                    'method': api_request.method,
                    'body': api_request.body,
                },
                'response': response_data,
            }
        )

        message = error_message or default_message

        rollbar.report_message(message, request=request, extra_data=extra_data)

    def handle_response(self, response):
        try:
            response_json = response.json()
            is_bad_response = type(response_json) == dict and response_json.get('error')
        except ValueError:
            is_bad_response = True
            response_json = {}

        if is_bad_response:
            self.handle_bad_response(response, response_json=response_json)
        else:
            pass

        return response_json

    def request_get(
        self, request_url=None, params=None, should_retry=True, **kwargs
    ):
        if request_url is None:
            request_url = self.get_request_url()

        headers = self.make_request_headers(action='GET')

        bad_response = False

        attempts = 0
        while should_retry:
            attempts += 1
            response = requests.get(
                request_url,
                headers=headers,
                params=params,
                allow_redirects=True,
                **kwargs
            )

            try:
                response_json = response.json()
            except ValueError:
                response_json = None

            if response.status_code < 400:
                should_retry = False
                bad_response = response_json is None or (
                    type(response_json) == dict and response_json.get('error')
                )
            elif 400 <= response.status_code < 500:
                if (
                    response.status_code == 429
                    and attempts < MAX_RETRY_ATTEMPTS
                ):
                    should_retry = True
                    time.sleep(2 ** (attempts - 1))
                else:
                    bad_response = True
                    should_retry = False
            elif 500 >= response.status_code:
                bad_response = True
                should_retry = False

        if bad_response:
            self.handle_bad_response(response, response_json=response_json)
            response_json = None
        else:
            pass

        return response_json

    def request_post(self, request_url=None, data=None, **kwargs):
        if request_url is None:
            request_url = self.get_request_url()

        headers = self.make_request_headers(action='POST')
        response = requests.post(
            request_url, headers=headers, json=data, **kwargs
        )
        response_json = self.handle_response(response)

        return response_json

    def request_put(self, request_url=None, data=None, **kwargs):
        if request_url is None:
            request_url = self.get_request_url()

        headers = self.make_request_headers(action='PUT')
        response = requests.put(
            request_url, headers=headers, json=data, **kwargs
        )
        response_json = self.handle_response(response)

        return response_json

    def request_delete(self, request_url=None, **kwargs):
        if request_url is None:
            request_url = self.get_request_url()

        headers = self.make_request_headers(action='DELETE')
        response = requests.delete(request_url, headers=headers, **kwargs)
        response_json = self.handle_response(response)

        return response_json

    ##
    # Users

    def get_user(self, user_id):
        resource_path = DSS_321FORMS_API_RESOURCE_USER % {
            'user_id': user_id,
        }
        request_url = self.get_request_url(resource_path=resource_path)
        response_json = self.request_get(request_url)
        user = response_json
        return user

    def get_user_everify(self, user_id):
        resource_path = DSS_321FORMS_API_RESOURCE_USER_EVERIFY % {
            'user_id': user_id,
        }
        request_url = self.get_request_url(resource_path=resource_path)
        response_json = self.request_get(request_url)
        everify_status = response_json
        return everify_status

    def get_users_by_company(self, company_id, user_type):
        """Returns a list of users in a company based on `user_type` provided.

        Only shows users that the requesting account is allowed to manage
        """
        resource_path = DSS_321FORMS_API_RESOURCE_COMPANY_USERS % {
            'company_id': company_id,
            'user_type': user_type,
        }

        offset = 0
        limit = 50

        users = []

        while offset is not None:
            params = {
                'offset': offset,
                'limit': limit,
            }

            request_url = self.get_request_url(resource_path=resource_path)
            response_json = self.request_get(request_url, params=params)
            if type(response_json) == list:
                if len(response_json) == limit:
                    offset += limit
                else:
                    offset = None
                users.extend(response_json)
            else:
                offset = None

                if type(response_json) == dict and 'message' in response_json:
                    message = response_json['message']
                else:
                    message = 'Error retrieving users by company'

                extra_data = {
                    'username': self.username,
                    'company_id': company_id,
                    'user_type': user_type,
                }
                rollbar.report_message(message, extra_data=extra_data)

        return users

    def create_employee(self, user_id, employee_data):
        resource_path = DSS_321FORMS_API_RESOURCE_USER % {
            'user_id': user_id,
        }
        request_url = self.get_request_url(resource_path=resource_path)
        response_json = self.request_post(request_url, employee_data)
        employee = response_json
        return employee

    def get_hr_staff_users_by_company(self, company_id):
        return self.get_users_by_company(
            company_id, DSS_321FORMS_API_USER_TYPE_HR_STAFF
        )

    def get_hr_admin_users_by_company(self, company_id):
        return self.get_users_by_company(
            company_id, DSS_321FORMS_API_USER_TYPE_HR_ADMIN
        )

    def get_employee_users_by_company(self, company_id):
        return self.get_users_by_company(
            company_id, DSS_321FORMS_API_USER_TYPE_EMPLOYEE
        )

    def get_onboarded_employee_users_by_company(self, company_id):
        """Returns a list of 100% onboarded users in the provided company.

        Sorted by latest approved form date (provided in response as 'utc_latest_approved_date')
        """
        return self.get_users_by_company(
            company_id, DSS_321FORMS_API_USER_TYPE_EMPLOYEE_COMPLETE
        )

    ##
    # Companies

    def get_companies(self):
        """Returns a JSON response of companies that the user can access"""
        offset = 0
        limit = 50

        all_companies = []

        done = False
        while not done:
            request_url = self.get_request_url(
                resource_path=DSS_321FORMS_API_RESOURCE_COMPANY
            ) + (
                "?limit=%s&offset=%s"
                % (
                    limit,
                    offset,
                )
            )
            response_json = self.request_get(request_url)
            companies = response_json or []
            all_companies.extend(companies)

            if len(companies) < limit:
                done = True
            else:
                offset += limit

        return all_companies

    ##
    # Divisions

    def get_divisions_by_company(self, company_id):
        """Returns a JSON response with two elements. The companyID provided and an array of divisions"""
        resource_path = DSS_321FORMS_API_RESOURCE_COMPANY_DIVISIONS % {
            'company_id': company_id,
        }
        request_url = self.get_request_url(resource_path=resource_path)
        response_json = self.request_get(request_url) or {}

        divisions = response_json.get('divisions', [])
        return divisions

    ##
    # Forms

    def get_forms_by_company(self, company_id):
        """Returns an array of the company's forms.

        This will be used when selecting the forms to provide for a new hire
        """
        resource_path = DSS_321FORMS_API_RESOURCE_COMPANY_FORMS % {
            'company_id': company_id,
        }
        request_url = self.get_request_url(resource_path=resource_path)
        response_json = self.request_get(request_url)
        forms = response_json or []
        return forms

    def get_form_by_company(self, company_id, form_id, form_type='questions'):
        """Returns an array of form questions and an object with the basic details of the form itself

        `form_type` can be one of:
        - 'questions': The list of questions that will be asked of the employee
        - 'pdf': The blank version of the PDF
        - 'resolution': The list of questions asked of the HR manager when resolving the form
        """
        resource_path = DSS_321FORMS_API_RESOURCE_COMPANY_FORM % {
            'company_id': company_id,
            'form_id': form_id,
        }
        request_url = self.get_request_url(resource_path=resource_path)

        params = {
            'type': form_type,
        }

        response_json = self.request_get(request_url, params=params)
        form = response_json
        return form

    def get_combined_form_by_company(self, company_id, form_id):
        questions_form = self.get_form_by_company(
            company_id, form_id, form_type='questions'
        )
        resolution_form = self.get_form_by_company(
            company_id, form_id, form_type='resolution'
        )

        combined_form = {}
        combined_form.update(questions_form)
        combined_questions = (
            questions_form['form_questions'] + resolution_form['form_questions']
        )

        combined_form['form_questions'] = combined_questions

        return combined_form

    def get_forms_by_division(self, division_id):
        resource_path = DSS_321FORMS_API_RESOURCE_DIVISION_FORMS % {
            'division_id': division_id,
        }
        request_url = self.get_request_url(resource_path=resource_path)
        response_json = self.request_get(request_url)
        forms = response_json or []
        return forms

    def get_forms_by_user(self, user_id):
        resource_path = DSS_321FORMS_API_RESOURCE_USER_FORMS % {
            'user_id': user_id,
        }
        request_url = self.get_request_url(resource_path=resource_path)
        response_json = self.request_get(request_url)
        forms = response_json or []
        return forms

    def get_form_by_user(
        self, user_id, form_id, form_type='questions', status='approved'
    ):
        """Receives response information of a user's latest form of a particular status

        `form_type` can be one of:
        - 'questions': list of question_number/response
        - 'fields': list of field name/value
        - 'pdf': base64encoded filled version of PDF
        - 'url': Temporary URL to download PDF

        `status` can be one of:
        - 'approved': Latest approved form
        - 'submitted': Latest submitted form
        """
        resource_path = DSS_321FORMS_API_RESOURCE_USER_FORM % {
            'user_id': user_id,
            'form_id': form_id,
        }
        request_url = self.get_request_url(resource_path=resource_path)

        params = {
            'type': form_type,
            'status': status,
        }

        response_json = self.request_get(request_url, params=params)
        forms = response_json or {}
        return forms

    ##
    # Responses

    def get_responses_by_user(
        self, user_id, questions=None, offset=0, limit=100
    ):
        """Receives response information to questions asked of a user

        `questions` a list of question ids  for which to return responses
        """
        resource_path = DSS_321FORMS_API_RESOURCE_USER_RESPONSES % {
            'user_id': user_id,
        }

        request_url = self.get_request_url(resource_path=resource_path)

        params = {
            'offset': offset,
            'limit': limit,
        }
        if questions:
            params['questions'] = questions

        response_json = self.request_get(request_url, params=params)
        user_responses = response_json or []
        return user_responses

    def get_all_responses_by_user(self, user_id, questions=None):
        all_responses = []

        offset = 0
        limit = 500
        should_fetch = True

        while should_fetch:
            user_responses = self.get_responses_by_user(
                self.username, offset=offset, limit=limit
            )
            all_responses.extend(user_responses)
            if len(user_responses) == limit:
                # get next page of responses
                should_fetch = True
                # 321Forms has a rate limit of 1 req/second per API account
                time.sleep(1)
                offset = offset + limit
            else:
                # stop fetching
                should_fetch = False

        return all_responses

    ##
    # Hooks / Webhooks

    def get_webhooks_by_company(self, company_id):
        resource_path = DSS_321FORMS_API_RESOURCE_COMPANY_WEBHOOKS % {
            'company_id': company_id,
        }

        request_url = self.get_request_url(resource_path=resource_path)

        response_json = self.request_get(request_url) or []
        return response_json

    def get_webhook(self, company_id, webhook_id):
        resource_path = DSS_321FORMS_API_RESOURCE_COMPANY_WEBHOOK % {
            'company_id': company_id,
            'webhook_id': webhook_id,
        }

        request_url = self.get_request_url(resource_path=resource_path)

        response_json = self.request_get(request_url)
        return response_json

    def get_webhook_topics(self, company_id):
        resource_path = DSS_321FORMS_API_RESOURCE_COMPANY_WEBHOOK_TOPICS % {
            'company_id': company_id,
        }

        request_url = self.get_request_url(resource_path=resource_path)

        response_json = self.request_get(request_url)
        webhook_topics = response_json or []

        return webhook_topics

    def create_webhook(self, company_id, url, topic_ids):
        resource_path = DSS_321FORMS_API_RESOURCE_COMPANY_WEBHOOKS % {
            'company_id': company_id,
        }

        request_url = self.get_request_url(resource_path=resource_path)

        data = {
            'url': url,
            'topics': topic_ids,
        }

        response_json = self.request_post(request_url, data=data)
        return response_json

    def update_webhook(self, company_id, webhook_id, url, topic_ids):
        resource_path = DSS_321FORMS_API_RESOURCE_COMPANY_WEBHOOK % {
            'company_id': company_id,
            'webhook_id': webhook_id,
        }

        request_url = self.get_request_url(resource_path=resource_path)

        data = {
            'url': url,
            'topics': topic_ids,
        }

        response_json = self.request_put(request_url, data=data)

        return response_json

    def delete_webhook(self, company_id, webhook_id):
        resource_path = DSS_321FORMS_API_RESOURCE_COMPANY_WEBHOOK % {
            'company_id': company_id,
            'webhook_id': webhook_id,
        }

        request_url = self.get_request_url(resource_path=resource_path)

        response_json = self.request_delete(request_url)
        return response_json

    ##
    # SSO - Single Sign-On

    def generate_sso_key(self):
        request_url = self.get_request_url(
            resource_path=DSS_321FORMS_API_RESOURCE_SSO_GENERATE
        )
        response_json = self.request_get(request_url) or {}

        sso_key = response_json.get('SSOKey')
        return sso_key

    def create_sso_endpoint(self, sso_key):
        resource_path = DSS_321FORMS_API_RESOURCE_SSO_ENDPOINT % {
            'sso_key': sso_key,
        }
        request_url = self.get_request_url(resource_path=resource_path)
        response_json = self.request_post(request_url) or {}
        endpoint = response_json.get('endpoint')

        return endpoint
