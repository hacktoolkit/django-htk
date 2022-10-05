# Python Standard Library Imports

# Third Party (PyPI) Imports
import rollbar

# Django Imports
from django.apps import AppConfig
from django.conf import settings
from django.contrib.auth import get_user_model
from django.db.models import signals

# HTK Imports
from htk.app_config import HtkAppConfig
from htk.apps.sites.utils import get_site_name
from htk.decorators.classes import disable_for_loaddata
from htk.utils import htk_setting


# isort: off


################################################################################
# signals and signal handlers


@disable_for_loaddata
def create_user_profile(sender, instance, created, **kwargs):
    """signal handler for User post-save"""
    if created:
        user = instance
        from htk.apps.accounts.utils.general import get_user_profile_model

        UserProfileModel = get_user_profile_model()
        profile = UserProfileModel.objects.create(user=user)
        profile.save()
        if not settings.TEST and htk_setting('HTK_SLACK_NOTIFICATIONS_ENABLED'):
            try:
                from htk.utils.notifications import slack_notify

                slack_notify(
                    'A new user has registered on the site %s: *%s <%s>*'
                    % (
                        get_site_name(),
                        user.profile.get_display_name(),
                        user.email,
                    )
                )
                if htk_setting('HTK_SLACK_BOT_ENABLED'):
                    slack_notify('htk: emaildig %s' % user.email)
            except:
                rollbar.report_exc_info()

        if not settings.TEST and htk_setting('HTK_ITERABLE_ENABLED'):
            try:
                from htk.lib.iterable.utils import get_iterable_api_client

                itbl = get_iterable_api_client()
                itbl.notify_sign_up(user)
            except:
                rollbar.report_exc_info()

        if htk_setting('HTK_INVITATIONS_LIFECYCLE_SIGNALS_ENABLED'):
            from htk.apps.invitations.services import InvitationsService

            invitations_service = InvitationsService()
            invitations_service.process_user_created(user)


def pre_delete_user(sender, instance, using, **kwargs):
    user = instance
    if not settings.TEST and htk_setting('HTK_ITERABLE_ENABLED'):
        try:
            from htk.lib.iterable.utils import get_iterable_api_client

            itbl = get_iterable_api_client()
            emails = list(
                set(
                    [user.email]
                    + [
                        user_email.email
                        for user_email in user.profile.get_confirmed_emails()
                    ]
                )
            )
            for email in emails:
                itbl.delete_user(email)
        except:
            rollbar.report_exc_info()


@disable_for_loaddata
def process_user_email_association(sender, instance, created, **kwargs):
    """signal handler for UserEmail post-save"""
    user_email = instance
    if user_email.is_confirmed:
        if htk_setting('HTK_INVITATIONS_LIFECYCLE_SIGNALS_ENABLED'):
            from htk.apps.invitations.services import InvitationsService

            invitations_service = InvitationsService()
            invitations_service.process_user_email_confirmation(user_email)


class HtkAccountsAppConfig(HtkAppConfig):
    name = 'htk.apps.accounts'
    verbose_name = 'Accounts'

    def ready(self):
        ##
        # signals
        UserModel = get_user_model()
        from htk.apps.accounts.models import UserEmail

        # Upon saving a User object, create a UserProfile object if it doesn't already exist
        signals.post_save.connect(
            create_user_profile,
            sender=UserModel,
            dispatch_uid='htk_create_user_profile',
        )
        # See AUTH_PROFILE_MODULE in settings.py

        signals.pre_delete.connect(
            pre_delete_user,
            sender=UserModel,
            dispatch_uid='htk_pre_delete_user',
        )

        signals.post_save.connect(
            process_user_email_association,
            sender=UserEmail,
            dispatch_uid='htk_process_user_email_association',
        )
