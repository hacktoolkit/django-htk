# Python Standard Library Imports
from enum import Enum


class OrganizationMemberRoles(Enum):
    SYSADMIN = 0
    OWNER = 1
    ADMIN = 10
    MEMBER = 100

    @classmethod
    def hidden_choices(cls):
        hidden = {
            OrganizationMemberRoles.SYSADMIN,
        }
        return hidden

    def is_hidden(self):
        return self in self.hidden_choices()


class OrganizationTeamMemberRoles(Enum):
    ADMIN = 10
    MEMBER = 100
