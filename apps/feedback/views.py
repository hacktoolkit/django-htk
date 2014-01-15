from django.contrib.sites.models import get_current_site
from django.views.decorators.http import require_POST

from htk.api.constants import *
from htk.api.utils import json_response_error
from htk.api.utils import json_response_okay

from htk.apps.feedback.forms import FeedbackForm

@require_POST
def submit(request):
    success = False

    antispam = request.POST.get(HTK_API_KEY_ANTISPAM) == HTK_API_VALUE_ANTISPAM_CHALLENGE_RESPONSE
    feedback_form = FeedbackForm(request.POST)
    if antispam and feedback_form.is_valid():
        site = get_current_site(request)
        success = True
        uri = request.META['HTTP_REFERER']
        feedback = feedback_form.save(site, uri)
    data = {}
    if success:
        response = json_response_okay()
    else:
        response = json_response_error()
    return response
