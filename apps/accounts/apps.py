from django.apps import AppConfig
from django.contrib.auth import get_user_model
from django.db.models import signals

from htk.apps.accounts.models import UserEmail
from htk.apps.accounts.utils.general import get_user_profile_model
from htk.utils import htk_setting
from htk.utils.notifications import slack_notify

################################################################################
# signals and signal handlers

def create_user_profile(sender, instance, created, **kwargs):
    """signal handler for User post-save
    """
    if created:
        user = instance
        UserProfileModel = get_user_profile_model()
        profile = UserProfileModel.objects.create(user=user)
        profile.save()
        if htk_setting('HTK_SLACK_NOTIFICATIONS_ENABLED'):
            slack_notify('A new user has registered on the site: *%s <%s>*' % (user.profile.get_display_name(), user.email,))

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

        # Upon saving a User object, create a UserProfile object if it doesn't already exist
        signals.post_save.connect(create_user_profile, sender=UserModel)
        # See AUTH_PROFILE_MODULE in settings.py

        signals.post_save.connect(process_user_email_association, sender=UserEmail)
