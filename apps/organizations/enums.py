from enum import Enum

class OrganizationMemberRoles(Enum):
    OWNER = 1
    MEMBER = 100

class OrganizationTeamMemberRoles(Enum):
    OWNER = 1
    ADMIN = 10
    MEMBER = 100
