# Third Party (PyPI) Imports
import rollbar

# Django Imports
from django.apps import AppConfig
from django.conf import settings
from django.db.models import signals

# HTK Imports
from htk.app_config import HtkAppConfig
from htk.decorators.classes import disable_for_loaddata
from htk.utils import (
    htk_setting,
    resolve_model_dynamically,
)


# isort: off


@disable_for_loaddata
def organization_invitation_updated(sender, instance, created, **kwargs):
    """Signal handler for when a new OrganizationInvitation object is created or updated"""
    invitation = instance
    if not settings.TEST and htk_setting('HTK_SLACK_NOTIFICATIONS_ENABLED'):
        from htk.utils.notifications import slack_notify

        if created:
            msg = invitation.build_notification_message__created()
        else:
            INVITATION_ACCEPTANCE_MESSAGE_BUILDERS = {
                True: invitation.build_notification_message__accepted,
                False: invitation.build_notification_message__declined,
                None: invitation.build_notification_message__resent,
            }
            msg_builder = INVITATION_ACCEPTANCE_MESSAGE_BUILDERS.get(invitation.accepted)

        if msg_builder is not None:
            msg = msg_builder()
            try:
                slack_notify(msg)
            except Exception:
                rollbar.report_exc_info()

class HtkOrganizationAppConfig(HtkAppConfig):
    name = 'htk.apps.organizations'
    label = 'organizations'
    verbose_name = 'Organizations'

    def ready(self):
        OrganizationInvitation = resolve_model_dynamically(
            htk_setting('HTK_ORGANIZATION_INVITATION_MODEL')
        )

        signals.post_save.connect(
            organization_invitation_created,
            sender=OrganizationInvitation,
            dispatch_uid='htk_organization_invitation_created',
        )
