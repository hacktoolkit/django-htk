# Django Imports
from django.http import (
    Http404,
    HttpResponse,
)
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST

# HTK Imports
from htk.api.utils import (
    extract_post_params,
    json_response,
)
from htk.lib.slack.constants import SLACK_WEBHOOK_PARAMS
from htk.lib.slack.utils import is_valid_webhook_event


# isort: off


@require_POST
@csrf_exempt
def slack_webhook_view(request):
    """Handles a Slack webhook request

    https://api.slack.com/outgoing-webhooks
    """
    event = extract_post_params(request.POST, SLACK_WEBHOOK_PARAMS)
    if is_valid_webhook_event(event, request):
        from htk.lib.slack.utils import handle_event
        payload = handle_event(event)
        if payload:
            response = json_response(payload)
        else:
            response = HttpResponse(status=200)
    else:
        raise Http404
    return response
