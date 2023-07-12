# Python Standard Library Imports
from typing import Any

# Django Imports
from django.core.exceptions import ValidationError
from django.core.validators import (
    MaxValueValidator,
    MinValueValidator,
)
from django.db import models
from django.db.models.fields.related import ForeignKey
from django.db.utils import ConnectionRouter


class CrossDBForeignKey(ForeignKey):
    """
    Django does not support for field relations between databases (See Reference 1)
    This is a work around to overcome the obstacle without needing to change
    any Django core files.

    Also it sets `db_constraint` to `False` so that it will not create Foreign Keys
    in database.

    Reference 1: https://docs.djangoproject.com/en/4.2/topics/db/multi-db/#limitations-of-multiple-databases
    Reference 2: https://stackoverflow.com/questions/6830564/how-to-use-django-models-with-foreign-keys-in-different-dbs
    """

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        if kwargs.get('db_constraint', None) is None:
            # If it is not specified explicitly set db_constraint to False
            # so that it will not create foreign keys in the DB.
            kwargs['db_constraint'] = False

        super().__init__(*args, **kwargs)

    def validate(self, value, model_instance) -> None:
        if self.remote_field.parent_link:
            return
        # Call the grandparent rather than the parent to skip validation
        super(ForeignKey, self).validate(value, model_instance)

        if value is None:
            return

        # This is the trick
        using = ConnectionRouter().db_for_read(
            self.remote_field.to, instance=model_instance
        )

        qs = self.remote_field.model._base_manager.using(using).filter(
            **{self.remote_field.field_name: value}
        )
        qs = qs.complex_filter(self.get_limit_choices_to())
        if not qs.exists():
            raise ValidationError(
                self.error_messages['invalid'],
                code='invalid',
                params={
                    'model': self.remote_field.model._meta.verbose_name,
                    'pk': value,
                    'field': self.remote_field.field_name,
                    'value': value,
                },  # 'pk' is included for backwards compatibility
            )


class StarRatingField(models.PositiveIntegerField):
    def __init__(self, min_value=1, max_value=5, *args, **kwargs):
        self.min_value = min_value
        self.max_value = max_value
        super(StarRatingField, self).__init__(
            blank=True,
            null=True,
            validators=[
                MinValueValidator(min_value),
                MaxValueValidator(max_value),
            ],
            *args,
            **kwargs,
        )

    def formfield(self, **kwargs):
        # HTK Imports
        import htk.forms.fields

        defaults = {
            'min_value': self.min_value,
            'max_value': self.max_value,
            'form_class': htk.forms.fields.StarRatingField,
        }
        defaults.update(kwargs)
        return super(StarRatingField, self).formfield(**defaults)


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
