# Python Standard Library Imports

# HTK Imports
from htk.utils.enums import get_enum_choices


def get_invitation_status_choices():
    from htk.apps.invitations.enums import InvitationStatus
    choices = get_enum_choices(InvitationStatus)
    return choices
