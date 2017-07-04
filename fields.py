from decimal import Decimal

from django.db import models

try:
    from south.modelsinspector import add_introspection_rules
except ImportError:
    SOUTH = False
else:
    SOUTH = True

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
