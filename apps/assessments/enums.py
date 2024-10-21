# Python Standard Library Imports
from enum import Enum


class QuestionType(Enum):
    UNSPECIFIED = 0
    FREE_RESPONSE = 1
    MULTIPLE_CHOICE = 2
    YES_OR_NO = 3

    MULTISELECT = 10

    TIME = 20
    DATE = 21
    DATETIME = 22

    FILE = 30
