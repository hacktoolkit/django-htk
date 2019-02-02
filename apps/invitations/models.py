# Python Standard Library Imports

# Third Party / PIP Imports

# Django Imports
from django.conf import settings
from django.db import models

# HTK Imports
from htk.apps.invitations.enums import InvitationStatus
from htk.apps.invitations.utils import get_invitation_status_choices
from htk.models.classes import HtkBaseModel
from htk.utils.cache_descriptors import CachedAttribute
from htk.utils.enums import get_enum_symbolic_name


class HtkInvitation(HtkBaseModel):
    email = models.EmailField(unique=True)
    first_name = models.CharField(max_length=30, blank=True)
    last_name = models.CharField(max_length=30, blank=True)
    invited_by = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='invitations_sent')
    campaign = models.CharField(max_length=127, blank=True)
    notes = models.CharField(max_length=127, blank=True)
    status = models.PositiveIntegerField(default=InvitationStatus.INITIAL.value, choices=get_invitation_status_choices())
    user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='invitations_accepted', blank=True, null=True, default=None)
    # meta
    created_at = models.DateTimeField(auto_now_add=True)
    timestamp = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True
        verbose_name = 'Invitation'

    def __unicode__(self):
        value = '%s (invited by %s)' % (
            self.email,
            self.invited_by.email,
        )
        return value

    @CachedAttribute
    def status_display(self):
        value = get_enum_symbolic_name(InvitationStatus(self.status))
        return value
