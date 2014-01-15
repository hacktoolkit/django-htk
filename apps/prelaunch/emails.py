from htk.apps.prelaunch.constants import *
from htk.mailers import send_email
from htk.utils import htk_setting

def prelaunch_email(prelaunch_signup):
    subject = htk_setting('HTK_PRELAUNCH_EMAIL_SUBJECT', HTK_PRELAUNCH_EMAIL_SUBJECT)
    bcc = htk_setting('HTK_PRELAUNCH_EMAIL_BCC', HTK_PRELAUNCH_EMAIL_BCC)
    context = {
        'prelaunch_signup': prelaunch_signup,
    }
    send_email(
        template='prelaunch',
        subject=subject,
        to=[prelaunch_signup.email,],
        bcc=bcc,
        context=context
    )
