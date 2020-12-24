# Python Standard Library Imports
import json

# Third Party (PyPI) Imports
from pydantic import BaseModel

# HTK Imports
from htk.api.utils import extract_post_params
from htk.lib.discord.constants import DISCORD_WEBHOOK_RELAY_PARAMS


# isort: off


class Relay(BaseModel):
    webhook_id: str
    webhook_token: str
    content: str


def validate_relay_request(request):
    request_json = json.loads(request.body)
    relay = Relay(**request_json)

    return relay
