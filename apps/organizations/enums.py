# Python Standard Library Imports
from enum import Enum


class OrganizationMemberRoles(Enum):
    OWNER = 1
    ADMIN = 10
    MEMBER = 100

class OrganizationTeamMemberRoles(Enum):
    ADMIN = 10
    MEMBER = 100
