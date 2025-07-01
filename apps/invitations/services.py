# Python Standard Library Imports

# HTK Imports
from htk.apps.sites.utils import get_site_name
from htk.services import HtkBaseService
from htk.utils import htk_setting
from htk.utils.notifications import slack_notify


# isort: off


class InvitationsService(HtkBaseService):
    def __init__(self, *args, **kwargs):
        super(InvitationsService, self).__init__(*args, **kwargs)
        models = htk_setting('HTK_INVITATION_MODELS') or [
            htk_setting('HTK_INVITATION_MODEL')
        ]
        if isinstance(models, (list, tuple)):
            self.init_models(models)
        else:
            raise TypeError('Improperly configured `HTK_INVITATION_MODELS`')

    def process_user_created(self, user):
        """Invoked when `user` is created

        Notification only, no other data/model side-effects
        """
        email = user.email
        if email:
            for model in self.models:
                q = model.objects.filter(email=email)
                if q.exists():
                    invitation = q.first()

                    # The email is not confirmed yet, just send a notification, but do not associate yet.

                    msg = (
                        '*%s* has signed up for %s as a result of an invitation from *%s <%s>* (Campaign: `%s` - sent %s).'
                        % (
                            email,
                            get_site_name(),
                            invitation.invited_by.profile.display_name,
                            invitation.invited_by.email,
                            invitation.campaign or 'None',
                            invitation.get_relative_time(),
                        )
                    )
                    slack_notify(msg)

    def process_user_email_confirmation(self, user_email):
        """Invoked when `user_email` is confirmed

        Calls `Invitation.connect_user()`
        """
        assert user_email.is_confirmed

        user = user_email.user
        email = user_email.email

        for model in self.models:
            q = model.objects.filter(email=email)
            if q.exists():
                invitation = q.first()
                invitation.connect_user(user)

    def process_user_completed(self, user):
        """Invoked when `user` completely satisfies the onboarding requirements of the invitation flow

        Calls `Invitation.complete()`
        """
        email = user.email
        if email:
            for model in self.models:
                q = model.objects.filter(email=email)
                if q.exists():
                    invitation = q.first()
                    invitation.complete(user)
