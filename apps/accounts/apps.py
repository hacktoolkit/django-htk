import rollbar

from django.apps import AppConfig
from django.contrib.auth import get_user_model
from django.db.models import signals

from htk.utils import htk_setting

################################################################################
# signals and signal handlers

def create_user_profile(sender, instance, created, **kwargs):
    """signal handler for User post-save
    """
    if created:
        user = instance
        from htk.apps.accounts.utils.general import get_user_profile_model
        UserProfileModel = get_user_profile_model()
        profile = UserProfileModel.objects.create(user=user)
        profile.save()
        if htk_setting('HTK_SLACK_NOTIFICATIONS_ENABLED'):
            try:
                from htk.utils.notifications import slack_notify
                slack_notify('A new user has registered on the site %s: *%s <%s>*' % (
                    htk_setting('HTK_SITE_NAME'),
                    user.profile.get_display_name(),
                    user.email,
                ))
            except:
                rollbar.report_exc_info()

        if htk_setting('HTK_ITERABLE_ENABLED'):
            try:
                from htk.lib.iterable.utils import get_iterable_api_client
                itbl = get_iterable_api_client()
                itbl.notify_sign_up(user)
            except:
                rollbar.report_exc_info()

def process_user_email_association(sender, instance, created, **kwargs):
    """signal handler for UserEmail post-save
    """
    user_email = instance
    if user_email.is_confirmed:
        user = user_email.user
        email = user_email.email
        #associate_invitations(user, email)

class HtkAccountsAppConfig(AppConfig):
    name = 'htk.apps.accounts'
    verbose_name = 'Accounts'

    def ready(self):
        ##
        # signals
        UserModel = get_user_model()
        from htk.apps.accounts.models import UserEmail

        # Upon saving a User object, create a UserProfile object if it doesn't already exist
        signals.post_save.connect(create_user_profile, sender=UserModel)
        # See AUTH_PROFILE_MODULE in settings.py

        signals.post_save.connect(process_user_email_association, sender=UserEmail)
