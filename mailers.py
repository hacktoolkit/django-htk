from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from django.core.mail import send_mail
from django.template import Context
from django.template.loader import get_template

from htk.constants.defaults import *
from htk.utils import htk_setting

def simple_email(
    subject='',
    message='',
    sender=None,
    to=None,
    fail_silently=False
    ):
    sender = sender or htk_setting('HTK_DEFAULT_EMAIL_SENDER', HTK_DEFAULT_EMAIL_SENDER)
    to = to or htk_setting('HTK_DEFAULT_EMAIL_RECIPIENTS', HTK_DEFAULT_EMAIL_RECIPIENTS)
    if settings.ENV_DEV:
        fail_silently = True
        subject = '[hacktoolkit-dev] %s' % subject
    send_mail(subject, message, sender, to, fail_silently = fail_silently)

def send_email(
    template=None,
    subject='',
    sender=None,
    to=None,
    cc=None,
    bcc=None,
    context=None,
    text_only=False
    ):
    template = template or 'base'
    sender = sender or htk_setting('HTK_DEFAULT_EMAIL_SENDER', HTK_DEFAULT_EMAIL_SENDER)
    to = to or htk_setting('HTK_DEFAULT_EMAIL_RECIPIENTS', HTK_DEFAULT_EMAIL_RECIPIENTS)
    bcc = bcc or []
    cc = cc or []
    context = context or {}
    c = Context(context)
    if settings.ENV_DEV:
        subject = '[hacktoolkit-dev] %s' % subject
    text_template = get_template("emails/%s.txt" % template)
    text_content = text_template.render(c)
    msg = EmailMultiAlternatives(subject=subject,
                                 body=text_content,
                                 from_email=sender,
                                 to=to,
                                 bcc=bcc,
                                 cc=cc)
    if not text_only:
        html_template = get_template("emails/%s.html" % template)
        html_content = html_template.render(c)
        msg.attach_alternative(html_content, 'text/html')
    msg.send()
