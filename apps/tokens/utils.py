# HTK Imports
from htk.utils import (
    htk_setting,
    resolve_model_dynamically,
)


def get_token_model():
    Token = resolve_model_dynamically(htk_setting('HTK_TOKEN_MODEL'))
    return Token


def get_valid_token_value(key):
    Token = get_token_model()

    try:
        token = Token.objects.get(key=key)
        value = token.value if token.is_valid else None
    except Token.DoesNotExist:
        value = None

    return value
