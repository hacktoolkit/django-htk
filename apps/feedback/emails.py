from htk.apps.feedback.constants import *
from htk.mailers import send_email
from htk.utils import htk_setting

def feedback_email(feedback):
    subject = htk_setting('HTK_FEEDBACK_EMAIL_SUBJECT', HTK_FEEDBACK_EMAIL_SUBJECT)
    to = htk_setting('HTK_FEEDBACK_EMAIL_TO', [])
    if to:
        context = {
            'feedback': feedback,
        }
        send_email(
            template='feedback',
            subject=subject,
            to=to,
            context=context
        )
