# Django Imports
from django.urls import reverse

# HTK Imports
from htk.apps.feedback.constants import *
from htk.mailers import send_email
from htk.utils import htk_setting


def feedback_email(feedback, domain=None):
    domain = domain or htk_setting('HTK_DEFAULT_DOMAIN')

    subject = htk_setting('HTK_FEEDBACK_EMAIL_SUBJECT', HTK_FEEDBACK_EMAIL_SUBJECT)
    to = htk_setting('HTK_FEEDBACK_EMAIL_TO', [])
    if to:
        context = {
            'feedback': feedback,
            'domain': domain,
        }
        send_email(
            template='htk/feedback',
            subject=subject,
            to=to,
            context=context
        )
