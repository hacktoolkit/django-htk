# Django Imports
from django.db import models

# HTK Imports
from htk.models.fk_fields import build_kwargs
from htk.utils import htk_setting


# isort: off


def fk_openai_system_prompt(
    related_name: str, required: bool = False
) -> models.ForeignKey:
    field = models.ForeignKey(
        htk_setting('HTK_OPENAI_SYSTEM_PROMPT_MODEL'),
        related_name=related_name,
        **build_kwargs(required=required),
    )
    return field
