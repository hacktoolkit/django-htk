# Django Imports
from django.db import models

# HTK Imports
from htk.models.fields import CrossDBForeignKey
from htk.models.fk_fields import build_kwargs
from htk.utils import htk_setting


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
