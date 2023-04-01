# HTK Imports
from htk.utils import (
    htk_setting,
    resolve_model_dynamically,
)


def get_token_model(model=None):
    if model is None:
        Token = resolve_model_dynamically(htk_setting('HTK_TOKEN_MODEL'))
    else:
        Token = model

    return Token


def get_token(key, model=None, **kwargs):
    Token = get_token_model(model=model)

    try:
        token = Token.objects.get(key=key, **kwargs)
    except Token.DoesNotExist:
        token = None

    return token


def set_token(
    key,
    value,
    description=None,
    valid_after=None,
    valid_until=None,
    model=None,
    **kwargs
):
    Token = get_token_model(model=model)

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
            valid_until=valid_until,
            **kwargs
        )

    return token


def get_valid_token_value(key, model=None, **kwargs):
    token = get_token(key, model=model, **kwargs)
    value = token.value if token and token.is_valid else None

    return value
