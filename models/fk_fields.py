# Python Standard Library Imports
import copy

# Django Imports
from django.conf import settings
from django.db import models

# HTK Imports
from htk.models.fields import CrossDBForeignKey
from htk.utils import htk_setting


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


def build_kwargs(required: bool = False, **kwargs) -> dict:
    combined_kwargs = copy.copy(
        REQUIRED_KWARGS if required else NOT_REQUIRED_KWARGS
    )
    for k, v in kwargs.items():
        combined_kwargs[k] = v
    return combined_kwargs


##
# Users


def fk_user(
    related_name: str, required: bool = False, cross_db: bool = False
) -> models.ForeignKey:
    fk_class = CrossDBForeignKey if cross_db else models.ForeignKey
    field = fk_class(
        settings.AUTH_USER_MODEL,
        related_name=related_name,
        **build_kwargs(required=required),
    )
    return field


##
# Organizations


def fk_organization(
    related_name: str,
    required: bool = False,
    cross_db: bool = False,
    **kwargs,
) -> models.ForeignKey:
    fk_class = CrossDBForeignKey if cross_db else models.ForeignKey
    field = fk_class(
        htk_setting('HTK_ORGANIZATION_MODEL'),
        related_name=related_name,
        **build_kwargs(required=required, **kwargs),
    )
    return field
