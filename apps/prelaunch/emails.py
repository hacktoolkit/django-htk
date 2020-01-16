# HTK Imports
from htk.apps.prelaunch.constants import *
from htk.mailers import send_email
from htk.utils import htk_setting


def prelaunch_email(prelaunch_signup):
    template = htk_setting('HTK_PRELAUNCH_EMAIL_TEMPLATE', HTK_PRELAUNCH_EMAIL_TEMPLATE)
    subject = htk_setting('HTK_PRELAUNCH_EMAIL_SUBJECT', HTK_PRELAUNCH_EMAIL_SUBJECT)
    bcc = htk_setting('HTK_PRELAUNCH_EMAIL_BCC', HTK_PRELAUNCH_EMAIL_BCC)

    context = {
        'prelaunch_signup': prelaunch_signup,
        'site_name': htk_setting('HTK_SITE_NAME')
    }
    send_email(
        template=template,
        subject=subject,
        to=[prelaunch_signup.email,],
        bcc=bcc,
        context=context
    )
