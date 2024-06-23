# Django Imports
from django.shortcuts import get_object_or_404

# HTK Imports
from htk.admintools.decorators import company_employee_required
from htk.api.utils import json_response_okay
from htk.apps.prelaunch.loading import PrelaunchSignup


@company_employee_required
def prelaunch_toggle_view(request, prelaunch_id):
    """Toggle the early access status of a PrelaunchSignup

    :param request: the HTTP request object
    :param prelaunch_id: the ID of the PrelaunchSignup
    """
    prelaunch_signup = get_object_or_404(PrelaunchSignup, id=prelaunch_id)
    prelaunch_signup.toggle_early_access()
    response = json_response_okay()
    return response
