# Django Imports
from django.core import exceptions
from django.db import models
from django.utils.translation import gettext_lazy as _

from .types import ULID


class ULIDField(models.CharField):
    """ULID Field"""

    description = _('Universally Unique Lexicographically Sortable Identifier')
    empty_strings_allowed = False

    default_error_messages = {
        'invalid': _('“%(value)s” is not a valid ULID.'),
    }
    description = _('Universally Unique Lexicographically Sortable Identifier')
    empty_strings_allowed = False

    def __init__(self, *args, **kwargs):
        kwargs['max_length'] = 26
        kwargs['unique'] = True
        kwargs['editable'] = False
        kwargs.setdefault('unique', True)
        kwargs.setdefault('default', ULIDField._default)
        self.validators = []
        super().__init__(*args, **kwargs)

    def deconstruct(self):
        name, path, args, kwargs = super().deconstruct()
        del kwargs['max_length']
        return name, path, args, kwargs

    def get_db_prep_value(self, value, connection, prepared=False):
        value = super().get_prep_value(value)
        if value is None:
            return value
        return str(value)

    def from_db_value(self, value, expression, connection):
        return self.to_python(value)

    def to_python(self, value):
        if value is not None:
            try:
                if isinstance(value, str):
                    return ULID.from_str(value)
                elif isinstance(value, bytes):
                    return ULID.from_bytes(value)
                elif isinstance(value, int):
                    return ULID.from_int(value)
            except ValueError:
                raise exceptions.ValidationError(
                    self.error_messages['invalid'],
                    code='invalid',
                    params={'value': value},
                )
        return value

    @staticmethod
    def _default():
        value = ULID()
        return str(value)
