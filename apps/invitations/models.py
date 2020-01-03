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
from htk.utils.datetime_utils import relative_time
from htk.utils.enums import get_enum_symbolic_name
from htk.utils import htk_setting


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

    def __str__(self):
        value = '%s (invited by %s)' % (
            self.email,
            self.invited_by.email,
        )
        return value

    @CachedAttribute
    def status_display(self):
        value = get_enum_symbolic_name(InvitationStatus(self.status))
        return value

    def get_relative_time(self):
        """Returns a string representing the relative duration of time between now and when the invitation was created
        """
        result = relative_time(self.created_at)
        return result

    ##
    # Outbound Actions

    def send(self):
        self.status = InvitationStatus.EMAIL_SENT.value
        self.save()

    ##
    # Lifecycle Methods

    def connect_user(self, user):
        """Connects `user` to this `Invitation`

        Sets status to `InvitationStatus.ACCEPTED`
        """
        self.user = user
        self.status = InvitationStatus.ACCEPTED.value
        self.save()

        if htk_setting('HTK_SLACK_NOTIFICATIONS_ENABLED'):
            from htk.utils.notifications import slack_notify

            msg = '*%s <%s>* has accepted an invitation from *%s <%s>* (Campaign: `%s` - sent %s).' % (
                user.profile.display_name,
                user.email,
                self.invited_by.profile.display_name,
                self.invited_by.email,
                self.campaign or 'None',
                self.get_relative_time(),
            )

            slack_notify(msg)

    def complete(self, user=None):
        """Completes the invitation lifecycle

        This should be invoked when `self.user` completely satisfies the onboarding requirements of the invitation flow

        Sets status to `InvitationStatus.COMPLETED`
        """
        if self.user is None and user is not None:
            self.user = user
        else:
            if user is not None:
                assert user == self.user

        assert self.user is not None

        self.status = InvitationStatus.COMPLETED.value
        self.save()

        if htk_setting('HTK_SLACK_NOTIFICATIONS_ENABLED'):
            from htk.utils.notifications import slack_notify

            msg = '*%s <%s>* has completed their invitation onboarding from *%s <%s>* (Campaign: `%s` - sent %s).' % (
                self.user.profile.display_name,
                self.user.email,
                self.invited_by.profile.display_name,
                self.invited_by.email,
                self.campaign or 'None',
                self.get_relative_time(),
            )

            slack_notify(msg)
