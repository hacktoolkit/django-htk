# Django Imports
from django.db import models

# HTK Imports
from htk.models.fk_fields import build_kwargs
from htk.utils import htk_setting


def fk_conversation(
    related_name: str,
    required: bool = False,
    **kwargs,
) -> models.ForeignKey:
    field = models.ForeignKey(
        htk_setting('HTK_CONVERSATION_MODEL'),
        related_name=related_name,
        **build_kwargs(required=required, **kwargs),
    )
    return field
