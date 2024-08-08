# Python Standard Library Imports
import datetime

# Django Imports
from django.urls import reverse
from django.utils.http import int_to_base36

# HTK Imports
from htk.emails import BaseBatchRelationshipEmails
from htk.mailers import send_email
from htk.utils import htk_setting
from htk.utils import utcnow


class AccountActivationReminderEmails(BaseBatchRelationshipEmails):
    def __init__(self):
        from htk.apps.accounts.cachekeys import AccountActivationReminderEmailCooldown
        template = htk_setting('HTK_ACCOUNT_ACTIVATION_REMINDER_EMAIL_TEMPLATE')
        super(AccountActivationReminderEmails, self).__init__(
            cooldown_class=AccountActivationReminderEmailCooldown,
            template=template
        )

    def get_recipients(self):
        from htk.apps.accounts.utils.lookup import get_inactive_users
        inactive_users = get_inactive_users()
        # send reminders after 1 day and up to 3 weeks
        account_creation_threshold_upper = utcnow() - datetime.timedelta(days=1)
        account_creation_threshold_lower = account_creation_threshold_upper - datetime.timedelta(days=21)
        users = inactive_users.filter(
            date_joined__gte=account_creation_threshold_lower,
            date_joined__lte=account_creation_threshold_upper
        )
        return users

    def send_email(self, recipient, **kwargs):
        """Sends an activation reminder email to `recipient`, a Django User
        """
        user = recipient
        user.profile.send_activation_reminder_email()


def activation_email(user_email, use_https=False, domain=None, template=None, subject=None, sender=None):
    """Sends an activation/confirmation email for user to confirm email address
    """
    user = user_email.user
    email = user_email.email
    domain = domain or htk_setting('HTK_DEFAULT_EMAIL_SENDING_DOMAIN')

    context = {
        'user': user,
        'first_name': user.first_name,
        'last_name': user.last_name,
        'email': email,
        'protocol': use_https and 'https' or 'http',
        'domain': domain,
        'activation_uri': user_email.get_activation_uri(use_https=use_https, domain=domain),
        'site_name': htk_setting('HTK_SITE_NAME'),
    }

    if template is None:
        template = 'accounts/activation'

    if subject is None:
        subject = htk_setting('HTK_ACCOUNT_EMAIL_SUBJECT_ACTIVATION') % context

    if htk_setting('HTK_ACCOUNT_EMAIL_BCC_ACTIVATION'):
        bcc = htk_setting('HTK_DEFAULT_EMAIL_BCC')
    else:
        bcc = None
    send_email(
        template=template,
        subject=subject,
        sender=sender,
        to=[email,],
        context=context,
        bcc=bcc
    )

def welcome_email(user, template=None, subject=None, sender=None):
    context = {
        'user': user,
        'email': user.profile.confirmed_email or user.email,
        'first_name': user.first_name,
        'last_name': user.last_name,
        'site_name': htk_setting('HTK_SITE_NAME'),
    }
    if htk_setting('HTK_ACCOUNT_EMAIL_BCC_WELCOME'):
        bcc = htk_setting('HTK_DEFAULT_EMAIL_BCC')
    else:
        bcc = None
    template = template or 'accounts/welcome'
    subject = (subject or htk_setting('HTK_ACCOUNT_EMAIL_SUBJECT_WELCOME')) % context
    send_email(
        template=template,
        subject=subject,
        sender=sender,
        to=[user.email],
        context=context,
        bcc=bcc
    )


def password_reset_email(user, token_generator, use_https=False, domain=None, template=None, subject=None, sender=None):
    domain = domain or htk_setting('HTK_DEFAULT_DOMAIN')
    context = {
        'user': user,
        'email': user.profile.confirmed_email or user.email,
        'protocol': use_https and 'https' or 'http',
        'domain': domain,
        'site_name': htk_setting('HTK_SITE_NAME'),
        'reset_path': reverse(
            htk_setting('HTK_ACCOUNT_RESET_PASSWORD_URL_NAME')
        ),
        'uid': int_to_base36(user.id),
        'token': token_generator.make_token(user),
    }

    reset_uri = '%(protocol)s://%(domain)s%(reset_path)s?u=%(uid)s&t=%(token)s' % context
    context['reset_uri'] = reset_uri
    template = template or 'accounts/reset_password'
    subject = (subject or htk_setting('HTK_ACCOUNT_EMAIL_SUBJECT_PASSWORD_RESET')) % context
    send_email(
        template=template,
        subject=subject,
        sender=sender,
        to=[context['email']],
        context=context
    )


def password_changed_email(
    user,
    template=None,
):
    context = {
        'user': user,
        'email': user.profile.confirmed_email or user.email,
        'domain': htk_setting('HTK_DEFAULT_DOMAIN'),
        'site_name': htk_setting('HTK_SITE_NAME'),
    }
    subject = htk_setting('HTK_ACCOUNT_EMAIL_SUBJECT_PASSWORD_CHANGED') % context
    send_email(
        template=template or 'accounts/password_changed',
        subject=subject,
        to=[user.profile.confirmed_email or user.email],
        context=context
    )
