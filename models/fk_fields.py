# Django Imports
from django.conf import settings
from django.db import models


# isort: off


REQUIRED_KWARGS = {
    'null': False,
    'blank': False,
    'on_delete': models.CASCADE,
}


NOT_REQUIRED_KWARGS = {
    'null': True,
    'blank': True,
    'default': None,
    'on_delete': models.SET_DEFAULT,
}


def build_kwargs(required: bool = False) -> dict:
    kwargs = REQUIRED_KWARGS if required else NOT_REQUIRED_KWARGS
    return kwargs


##
# Users


def fk_user(related_name: str, required: bool = False) -> models.ForeignKey:
    field = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name=related_name,
        **build_kwargs(required=required),
    )
    return field
