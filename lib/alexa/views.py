import json

from django.http import Http404
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST

from htk.api.utils import extract_post_params
from htk.api.utils import json_response
from htk.lib.alexa.constants import *
from htk.lib.alexa.utils import is_valid_alexa_event

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
    if is_valid_alexa_event(event, request):
        payload = {
            'version' : '1.0',
            'response' : {
                'outputSpeech' : {
                    'type' : 'SSML',
                    'ssml' : '<speak>This is pretty cool. It works!</speak>',
                },
            },
        }
        response = json_response(payload)
    else:
        raise Http404
    return response
