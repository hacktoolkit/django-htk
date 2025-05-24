# Django Imports
from django.core.validators import (
    MaxValueValidator,
    MinValueValidator,
)
from django.db import models


class IntegerRangeField(models.IntegerField):
    def __init__(
        self,
        verbose_name=None,
        name=None,
        min_value=None,
        max_value=None,
        *args,
        **kwargs,
    ):
        self.min_value = min_value
        self.max_value = max_value

        validators = kwargs.pop('validators', [])
        if min_value:
            validators.append(MinValueValidator(min_value))
        if max_value:
            validators.append(MaxValueValidator(max_value))

        return super(IntegerRangeField, self).__init__(
            verbose_name=verbose_name,
            name=name,
            validators=validators,
            *args,
            **kwargs,
        )

    def formfield(self, **kwargs):
        defaults = {
            'min_value': self.min_value,
            'max_value': self.max_value,
        }
        defaults.update(kwargs)
        return super(IntegerRangeField, self).formfield(**defaults)
