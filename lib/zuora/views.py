# Python Standard Library Imports
import json

# Django Imports
from django.http import Http404
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST

# HTK Imports
from htk.lib.zuora.utils import get_event_handler


@require_POST
@csrf_exempt
def zuora_webhook_view(request):
    payload = json.loads(request.body)

    event_type = request.GET.get('event')
    if event_type is None:
        raise Http404

    event_handler = get_event_handler(event_type)
    if event_handler:
        event_handler(event_type, payload)

    response = HttpResponse(status=200)
    return response
