from hashlib import sha1
import datetime
import random

from django.core.urlresolvers import reverse
from django.utils.http import int_to_base36

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
        account_creation_threshold = utcnow() - datetime.timedelta(days=1)
        users = inactive_users.filter(
            date_joined__lte=account_creation_threshold
        )
        return users

    def send_email(self, recipient):
        """Sends an activation reminder email to `recipient`
        """
        recipient.profile.send_activation_reminder_email()

def activation_email(user_email, use_https=False, domain=None, template=None, subject=None):
    """Sends an activation/confirmation email for user to confirm email address
    """
    user = user_email.user
    email = user_email.email
    domain = domain or htk_setting('HTK_DEFAULT_EMAIL_SENDING_DOMAIN')

    context = {
        'user': user,
        'email': email,
        'protocol': use_https and 'https' or 'http', 
        'domain': domain,
        'site_name': htk_setting('HTK_SITE_NAME'),
        'confirm_email_path': reverse(
            htk_setting('HTK_ACCOUNTS_CONFIRM_EMAIL_URL_NAME'),
            args=(user_email.activation_key,)
        ),
    }

    if template is None:
        template='accounts/activation'

    if subject is None:
        'Confirm your email address, %s' % email

    activation_uri = '%(protocol)s://%(domain)s%(confirm_email_path)s' % context
    context['activation_uri'] = activation_uri
    bcc = htk_setting('HTK_DEFAULT_EMAIL_BCC')
    send_email(
        template=template,
        subject=subject,
        to=[email,],
        context=context,
        bcc=bcc
    )

def welcome_email(user):
    context = {
        'user': user,
        'site_name': htk_setting('HTK_SITE_NAME'),
    }
    bcc = htk_setting('HTK_DEFAULT_EMAIL_BCC')
    send_email(
        template='accounts/welcome',
        subject='Welcome to %s, %s' % (htk_setting('HTK_SITE_NAME'), user.email,),
        to=[user.email],
        context=context,
        bcc=bcc
    )

def password_reset_email(user, token_generator, use_https=False, domain=None):
    domain = domain or htk_setting('HTK_DEFAULT_DOMAIN')
    context = {
        'user': user,
        'email': user.email,
        'protocol': use_https and 'https' or 'http', 
        'domain': domain,
        'site_name': htk_setting('HTK_SITE_NAME'),
        'reset_path': reverse('account_reset_password'),
        'uid': int_to_base36(user.id),
        'token': token_generator.make_token(user),
    }

    reset_uri = '%(protocol)s://%(domain)s%(reset_path)s?u=%(uid)s&t=%(token)s' % context
    context['reset_uri'] = reset_uri
    send_email(
        template='accounts/reset_password',
        subject='Password reset on %s' % context['site_name'],
        to=[context['email']],
        context=context
    )

def password_changed_email(user):
    context = {
        'user': user,
        'email': user.email,
        'domain': htk_setting('HTK_DEFAULT_DOMAIN'),
        'site_name': htk_setting('HTK_SITE_NAME'),
    }
    send_email(
        template='accounts/password_changed',
        subject='Password changed on %s' % context['site_name'],
        to=[user.email],
        context=context
    )
