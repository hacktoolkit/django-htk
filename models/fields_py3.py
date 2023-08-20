"""This module requires Python major version >= 3
"""


# Python Standard Library Imports
import typing as T

# Django Imports
from django.db import models


# isort: off


class CrossDBForeignKey(models.ForeignKey):
    """
    Django does not support for field relations between databases (See Reference 1)
    This is a work around to overcome the obstacle without needing to change
    any Django core files.

    Also it sets `db_constraint` to `False` so that it will not create Foreign Keys
    in database.

    Reference 1: https://docs.djangoproject.com/en/4.2/topics/db/multi-db/#limitations-of-multiple-databases
    Reference 2: https://stackoverflow.com/questions/6830564/how-to-use-django-models-with-foreign-keys-in-different-dbs
    """

    def __init__(self, *args: T.Any, **kwargs: T.Any) -> None:
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
