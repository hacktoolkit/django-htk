# Python Standard Library Imports
import re
import typing as T
from dataclasses import dataclass
from enum import Enum

# Django Imports
from django.db import DatabaseError


# isort: off


class MySQLError(Enum):
    DUPLICATE_ENTRY = 1062


DUPLICATE_ENTRY_REGEX = re.compile(
    r'^Duplicate entry \'(?P<value>.+)\' for key \'(?P<app_label>[a-z]+)_(?P<model>[a-z]+)_(?P<field>.+)_(?P<index_uuid>.+)_uniq\'$'
)


@dataclass
class ParsedDatabaseError:
    code: str
    message: str

    @property
    def mysql_error(self) -> T.Optional[MySQLError]:
        try:
            error = MySQLError(self.code)
        except:
            error = None
        return error

    @property
    def is_duplicate_entry(self):
        return self.mysql_error == MySQLError.DUPLICATE_ENTRY

    @property
    def duplicate_entry_field(self):
        if self.is_duplicate_entry:
            m = DUPLICATE_ENTRY_REGEX.match(self.message)
            field = m.group('field')
            # value = m.group('value')
        else:
            field = None
        return field


def parse_database_error(e: DatabaseError):
    """ """
    error_code, error_message = e.args
    parsed_error = ParsedDatabaseError(
        code=int(error_code), message=error_message
    )
    return parsed_error
