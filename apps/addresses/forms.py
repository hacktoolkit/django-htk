# Django Imports
from django import forms

# HTK Imports
from htk.forms.classes import AbstractModelInstanceUpdateForm
from htk.utils import htk_setting
from htk.utils import resolve_model_dynamically


class PostalAddressForm(AbstractModelInstanceUpdateForm):
    class Meta:
        model = resolve_model_dynamically(htk_setting('HTK_POSTAL_ADDRESS_MODEL'))
        exclude = (
            'latitude',
            'longitude',
            'street_number',
            'street_name',
            'unit_type',
            'unit',
        )
