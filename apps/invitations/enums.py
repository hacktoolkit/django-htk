# Python Standard Library Imports
from enum import Enum


class InvitationStatus(Enum):
    INITIAL = 0
    EMAIL_SENT = 1
    EMAIL_RESENT = 2
    ACCEPTED = 3
    COMPLETED = 4
