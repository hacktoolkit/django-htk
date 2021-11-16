# HTK Imports
from htk.utils import (
    htk_setting,
    resolve_model_dynamically,
)


def get_token_model():
    Token = resolve_model_dynamically(htk_setting('HTK_TOKEN_MODEL'))
    return Token


def get_token(key):
    Token = get_token_model()

    try:
        token = Token.objects.get(key=key)
    except Token.DoesNotExist:
        token = None

    return token


def set_token(key, value, description=None, valid_after=None, valid_until=None):
    Token = get_token_model()

    try:
        token = Token.objects.get(key=key)
        token.value = value
        token.valid_after = valid_after
        token.valid_until = valid_until

        if description:
            token.description = description
        token.save()
    except Token.DoesNotExist:
        token = Token.objects.create(
            key=key,
            value=value,
            description=description or '',
            valid_after=valid_after,
            valid_until=valid_until
        )

    return token


def get_valid_token_value(key):
    token = get_token(key)
    value = (
        token.value
        if token and token.is_valid
        else None
    )

    return value
