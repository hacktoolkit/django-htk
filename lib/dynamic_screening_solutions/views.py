# Third Party (PyPI) Imports
import rollbar

# Django Imports
from django.http import HttpResponseForbidden
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST

# HTK Imports
from htk.api.utils import json_response_okay
from htk.lib.dynamic_screening_solutions.utils import handle_webhook_request
from htk.lib.dynamic_screening_solutions.utils import validate_webhook_request


@require_POST
@csrf_exempt
def dss_321forms_webhook_view(request):
    try:
        webhook_data = validate_webhook_request(request)

        if webhook_data:
            handle_webhook_request(webhook_data)
            response = json_response_okay()
        else:
            response = HttpResponseForbidden()
    except ValueError:
        rollbar.report_exc_info(request=request)
        response = json_response_okay()
    except Exception:
        rollbar.report_exc_info(request=request)
        response = json_response_okay()

    return response
