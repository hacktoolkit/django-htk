# Python Standard Library Imports
import gzip
from decimal import Decimal

# Django Imports
from django.db import models


# isort: off


try:
    from south.modelsinspector import add_introspection_rules
except ImportError:
    SOUTH = False
else:
    SOUTH = True


class CompressedBinaryField(models.BinaryField):
    """A binary field with gzip compression

    See:
    - https://docs.djangoproject.com/en/4.1/ref/models/fields/#binaryfield
    - https://gist.github.com/jontsai/57316aecf5397b35d58be55b7e6ea5b0

    NOTE: From above on Abusing BinaryField:

    Although you might think about storing files in the database,
    consider that it is bad design in 99% of the cases.
    This field is not a replacement for proper static files handling.
    """

    description = "A binary field with gzip compression"

    def from_db_value(self, value, expression, connection):
        """Converts `value` retrieved from DB

        See:
        - https://docs.djangoproject.com/en/3.2/ref/models/fields/#django.db.models.Field.from_db_value
        """
        python_value = None if value is None else gzip.decompress(value)
        return python_value

    def get_prep_value(self, value):
        """Converts `value` into format for storage in DB

        See:
        - https://docs.djangoproject.com/en/3.2/howto/custom-model-fields/#converting-python-objects-to-query-values
        - https://docs.djangoproject.com/en/3.2/ref/models/fields/#django.db.models.Field.get_prep_value
        """
        prep_value = None if value is None else gzip.compress(value)
        return prep_value


class CurrencyField(models.DecimalField):
    def __init__(self, verbose_name=None, name=None, **kwargs):
        decimal_places = kwargs.pop('decimal_places', 2)
        max_digits = kwargs.pop('max_digits', 10)

        super(CurrencyField, self).__init__(
            verbose_name=verbose_name,
            name=name,
            max_digits=max_digits,
            decimal_places=decimal_places,
            **kwargs
        )

    def to_python(self, value):
        try:
            return super(CurrencyField, self).to_python(value).quantize(Decimal('0.01'))
        except AttributeError:
            return None

if SOUTH:
    add_introspection_rules([
        (
            [CurrencyField],
            [],
            {
                'decimal_places': ['decimal_places', { 'default': '2' }],
                'max_digits': ['max_digits', { 'default': '10' }],
            },
        ),
    ], ['^htk\.fields\.CurrencyField'])
