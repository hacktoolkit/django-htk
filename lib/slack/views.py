from django.http import Http404
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST

from htk.api.utils import extract_post_params
from htk.api.utils import json_response
from htk.lib.slack.constants import *
from htk.lib.slack.utils import is_valid_webhook_token

@require_POST
@csrf_exempt
def slack_webhook_view(request):
    """Handles a Slack webhook request

    https://api.slack.com/outgoing-webhooks
    """
    event = extract_post_params(request.POST, SLACK_WEBHOOK_PARAMS)
    token = event['token']
    if is_valid_webhook_token(token):
        from htk.lib.slack.utils import handle_event
        payload = handle_event(event)
        if payload:
            response = json_response(payload)
        else:
            response = HttpResponse(status=200)
    else:
        raise Http404
    return response
