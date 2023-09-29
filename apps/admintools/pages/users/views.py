# Django Imports
from django.views import View
from django.utils.decorators import method_decorator

# HTK Imports
from htk.admintools.decorators import company_employee_required
from htk.api.utils import json_response_okay


@method_decorator(company_employee_required, name='dispatch')
class UsersView(View):
    def get(self, request, *args, **kwargs):
        response = json_response_okay({})
        return response


@method_decorator(company_employee_required, name='dispatch')
class UserView(View):
    def get(self, request, user_id=None, *args, **kwargs):
        response = json_response_okay({})
        return response
