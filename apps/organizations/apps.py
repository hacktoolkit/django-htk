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
def organization_invitation_created(sender, instance, created, **kwargs):
    """Signal handler for when a new OrganizationInvitation object is created or updated"""
    if created:
        invitation = instance

        if not settings.TEST and htk_setting('HTK_SLACK_NOTIFICATIONS_ENABLED'):
            try:
                from htk.utils.notifications import slack_notify

                msg = invitation.build_notification_message__created()
                slack_notify(msg)
            except:
                rollbar.report_exc_info()
    if created == False:
        invitation = instance

        if not settings.TEST and htk_setting('HTK_SLACK_NOTIFICATIONS_ENABLED'):
            if invitation.accepted == True:
                try:
                    from htk.utils.notifications import slack_notify

                    msg = invitation.build_notification_message__accepted()
                    slack_notify(msg)
                except:
                    rollbar.report_exc_info()
            if invitation.accepted == False:
                try:
                    from htk.utils.notifications import slack_notify

                    msg = invitation.build_notification_message__declined()
                    slack_notify(msg)
                except:
                    rollbar.report_exc_info()
            if invitation.accepted == True:
                try:
                    from htk.utils.notifications import slack_notify

                    msg = invitation.build_notification_message__resent()
                    slack_notify(msg)
                except:
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
