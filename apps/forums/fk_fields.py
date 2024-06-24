# Django Imports
from django.db import models

# HTK Imports
from htk.models.fk_fields import build_kwargs
from htk.utils import htk_setting


def fk_forum(
    related_name: str,
    required: bool = False,
    **kwargs,
) -> models.ForeignKey:
    field = models.ForeignKey(
        htk_setting('HTK_FORUM_MODEL'),
        related_name=related_name,
        **build_kwargs(required=required, **kwargs),
    )
    return field


def fk_forum_thread(
    related_name: str,
    required: bool = False,
    **kwargs,
) -> models.ForeignKey:
    field = models.ForeignKey(
        htk_setting('HTK_FORUM_THREAD_MODEL'),
        related_name=related_name,
        **build_kwargs(required=required, **kwargs),
    )
    return field


def forum_tag(**kwargs) -> models.ManyToManyField:
    field = models.ManyToManyField(
        htk_setting('HTK_FORUM_TAG_MODEL'),
        **kwargs,
    )
    return field
