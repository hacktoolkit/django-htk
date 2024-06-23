# HTK Imports
from htk.mailers import send_email
from htk.utils import htk_setting


# isort: off


def prelaunch_email(prelaunch_signup):
    template = htk_setting('HTK_PRELAUNCH_EMAIL_TEMPLATE')
    subject = htk_setting('HTK_PRELAUNCH_EMAIL_SUBJECT')
    bcc = htk_setting('HTK_PRELAUNCH_EMAIL_BCC')

    context = {
        'prelaunch_signup': prelaunch_signup,
        'site_name': htk_setting('HTK_SITE_NAME'),
    }

    send_email(
        template=template,
        subject=subject,
        to=[
            prelaunch_signup.email,
        ],
        bcc=bcc,
        context=context,
    )


def early_access_email(prelaunch_signup):
    template = htk_setting('HTK_PRELAUNCH_EARLY_ACCESS_EMAIL_TEMPLATE')
    subject = htk_setting('HTK_PRELAUNCH_EARLY_ACCESS_EMAIL_SUBJECT')
    bcc = htk_setting('HTK_PRELAUNCH_EMAIL_BCC')

    context = {
        'prelaunch_signup': prelaunch_signup,
        'site_name': htk_setting('HTK_SITE_NAME'),
    }

    send_email(
        template=template,
        subject=subject,
        to=[
            prelaunch_signup.email,
        ],
        bcc=bcc,
        context=context,
    )
