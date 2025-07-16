# Django Imports
from django.db import models

# HTK Imports
from htk.models.fk_fields import build_kwargs
from htk.utils import htk_setting


# isort: off


def fk_product_collection(
    related_name: str, required: bool = False
) -> models.ForeignKey:
    fk_model = htk_setting('HTK_STORE_PRODUCT_COLLECTION_MODEL')

    if fk_model is None:
        field = None
    else:
        field = models.ForeignKey(
            fk_model,
            related_name=related_name,
            **build_kwargs(required=required),
        )

    return field
