# Python Standard Library Imports
import hashlib
import hmac
import json

# HTK Imports
from htk.compat import (
    IS_PYTHON_3,
    b64encode,
)
from htk.utils import htk_setting
from htk.utils.general import resolve_method_dynamically


def validate_webhook_request(request):
    """Validates a 321Forms webhook request

    Returns a JSON request body if it is valid
    Otherwise, returns None
    """
    webhook_data = json.loads(request.body)
    company_id = webhook_data.get('company', {}).get('id')

    headers = request.META
    expected_signature = headers.get('HTTP_X_ONBOARDING_SIGNATURE', '')

    hash_key_retriever = resolve_method_dynamically(htk_setting('HTK_321FORMS_WEBHOOK_HASH_KEY_RETRIEVER'))
    hash_key = hash_key_retriever(company_id)

    # `hash_key` can be `None`. `hmac.new` does not do well with `None` value for both Python 2 and 3
    if hash_key:
        # Even for Python 2 it seems we need to convert the hash_key to bytes.
        # REFERENCES:
        # https://bugs.python.org/issue16063
        # https://stackoverflow.com/a/31572219
        hash_key = hash_key.encode() if IS_PYTHON_3 else bytes(hash_key)
        request_body = request.body.encode() if IS_PYTHON_3 else request.body

        hashed = hmac.new(hash_key, request_body, digestmod=hashlib.sha1).digest()

        signature = b64encode(hashed)

        is_valid = signature == expected_signature
    else:
        is_valid = False

    if is_valid:
        webhook_data = webhook_data
    else:
        webhook_data = None

    return webhook_data


def handle_webhook_request(webhook_data):
    topic = webhook_data.get('topic', None)

    event_handlers = htk_setting('HTK_321FORMS_WEBHOOK_EVENT_HANDLERS')

    event_handler_method = event_handlers.get(topic)
    event_handler = resolve_method_dynamically(event_handler_method) if event_handler_method else None

    if event_handler:
        event_handler(webhook_data)
    else:
        pass
