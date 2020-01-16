# Python Standard Library Imports
import json

# Django Imports
from django.http import Http404
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST

# HTK Imports
from htk.api.utils import extract_post_params
from htk.api.utils import json_response
from htk.lib.alexa.constants import *
from htk.lib.alexa.utils import is_valid_alexa_skill_webhook_event


@require_POST
@csrf_exempt
def alexa_skill_webhook_view(request):
    """Handles an Amazon Alexa skill webhook request

    Sample Request
    {
        "session": {
            "sessionId": "SessionId.XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX",
            "application": {
                "applicationId": "amzn1.ask.skill.XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX"
            },
            "attributes": {},
            "user": {
                "userId": "amzn1.ask.account.XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX"
            },
            "new": true
        },
        "request": {
            "type": "IntentRequest",
            "requestId": "EdwRequestId.XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX",
            "locale": "en-US",
            "timestamp": "2017-05-29T21:37:27Z",
            "intent": {
                "name": "ExampleIntent",
                "slots": {}
            }
        },
        "version": "1.0"
    }
    """
    request_json = json.loads(request.body)
    event = extract_post_params(request_json, ALEXA_SKILL_WEBHOOK_PARAMS)
    if is_valid_alexa_skill_webhook_event(event, request):
        from htk.lib.alexa.utils import handle_event
        payload = handle_event(event)
        if payload:
            response = json_response(payload)
        else:
            response = HttpResponse(status=200)
    else:
        raise Http404
    return response
