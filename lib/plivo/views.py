from django.http import Http404
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST

from htk.api.utils import extract_post_params
from htk.api.utils import json_response
from htk.lib.plivo.constants import *
from htk.lib.plivo.utils import handle_message_event

@require_POST
@csrf_exempt
def plivo_message_webhook_view(request):
    """Handles a Plivo webhook request

    https://www.plivo.com/docs/api/message/
    https://manage.plivo.com/app/
    """
    event = extract_post_params(request.POST, PLIVO_MESSAGE_WEBHOOK_PARAMS)
    result = handle_message_event(event)
    if result:
        response = HttpResponse(status=200)
    else:
        raise Http404
    return response
