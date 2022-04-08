# Third Party (PyPI) Imports
import requests

# Django Imports
from django.http import (
    Http404,
    HttpResponse,
)
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST

# HTK Imports
from htk.lib.discord.constants import DISCORD_WEBHOOK_URL
from htk.lib.discord.utils import validate_relay_request


# isort: off


@require_POST
@csrf_exempt
def discord_webhook_relay_view(request):
    """Handles a Discord webhook request

    https://discord.com/developers/docs/resources/webhook
    """
    relay = validate_relay_request(request)

    if relay:
        url = DISCORD_WEBHOOK_URL.format(
            webhook_id=relay.webhook_id,
            webhook_token=relay.webhook_token
        )

        payload = {}

        if relay.username:
            payload['username'] = relay.username

        if relay.embedded:
            # https://discord.com/developers/docs/resources/channel#embed-object
            payload['embeds'] = [
                {
                    'description': relay.content,
                },
            ]
        else:
            payload['content'] = relay.content

        try:
            webhook_response = requests.post(url, json=payload)

            response = HttpResponse(status=200)
        except Exception:
            response = HttpResponse(status=500)
    else:
        raise Http404

    return response
