# Python Standard Library Imports
import os
from email.mime.image import MIMEImage

# Django Imports
from django.conf import settings
from django.core.mail import (
    EmailMultiAlternatives,
    send_mail,
)
from django.template import TemplateDoesNotExist
from django.template.loader import get_template

# HTK Imports
from htk.constants.defaults import *
from htk.utils import htk_setting
from htk.utils.general import resolve_method_dynamically
from htk.utils.request import get_current_request
from htk.utils.text.converters import html2markdown


# isort: off


def simple_email(
    subject='',
    message='',
    sender=None,
    to=None,
    fail_silently=False
):
    """Sends a simple email
    """
    sender = sender or htk_setting('HTK_DEFAULT_EMAIL_SENDER', HTK_DEFAULT_EMAIL_SENDER)
    to = to or htk_setting('HTK_DEFAULT_EMAIL_RECIPIENTS', HTK_DEFAULT_EMAIL_RECIPIENTS)
    if settings.ENV_DEV:
        fail_silently = True
        subject = '[%s-dev] %s' % (htk_setting('HTK_SYMBOLIC_SITE_NAME'), subject,)
    send_mail(subject, message, sender, to, fail_silently=fail_silently)


def email_context_generator():
    """Default HTK email context generator
    Returns a dictionary with values for inflating templated emails
    """
    request = get_current_request()
    protocol = 'http'
    if request:
        if request.is_secure():
            protocol = 'https'
        else:
            pass
        domain = request.get_host() or htk_setting('HTK_DEFAULT_DOMAIN')
    else:
        domain = htk_setting('HTK_DEFAULT_DOMAIN')

    base_url = '%(protocol)s://%(domain)s' % {
        'protocol' : protocol,
        'domain' : domain,
    }

    context = {
        'base_url': base_url,
        'site_name': htk_setting('HTK_SITE_NAME'),
        'support_email': htk_setting('HTK_SUPPORT_EMAIL'),
    }
    return context


def get_email_context():
    """Get the email context dictionary for templated emails
    """
    email_context_generator = htk_setting('HTK_EMAIL_CONTEXT_GENERATOR')
    context = {}
    if email_context_generator:
        method = resolve_method_dynamically(email_context_generator)
        if method:
            context = method()
        else:
            pass
    else:
        pass
    return context


def attach_images_to_message(message, images):
    for image in images:
      fp = open(image, 'rb')
      filename = os.path.basename(image)
      msg_image = MIMEImage(fp.read())
      fp.close()
      msg_image.add_header('Content-ID', '<%s>' % filename)
      message.attach(msg_image)


def send_email(
    template=None,
    subject='',
    sender=None,
    reply_to=None,
    to=None,
    cc=None,
    bcc=None,
    context=None,
    text_only=False,
    headers=None
):
    """Sends a templated email w/ text and HTML
    """
    if headers is None:
        headers = {}

    if reply_to is not None:
        headers['Reply-To'] = reply_to

    template = template or 'base'
    sender = sender or htk_setting('HTK_DEFAULT_EMAIL_SENDER', HTK_DEFAULT_EMAIL_SENDER)
    to = to or htk_setting('HTK_DEFAULT_EMAIL_RECIPIENTS', HTK_DEFAULT_EMAIL_RECIPIENTS)
    bcc = bcc or []
    cc = cc or []

    base_context = get_email_context()
    if context:
        base_context.update(context)
    else:
        pass
    context = base_context

    if settings.ENV_DEV:
        subject = '[%s-dev] %s' % (htk_setting('HTK_SYMBOLIC_SITE_NAME'), subject,)

    # assume HTML template exists, get that first
    try:
        html_template = get_template('emails/%s.html' % template)
        context['base_template'] = htk_setting('HTK_EMAIL_BASE_TEMPLATE_HTML')
        html_content = html_template.render(context)
    except TemplateDoesNotExist:
        html_template = None
        html_content = ''

    # if native text template exists, use it
    try:
        context['base_template'] = htk_setting('HTK_EMAIL_BASE_TEMPLATE_TEXT')
        text_template = get_template('emails/%s.txt' % template)
        text_content = text_template.render(context)
    except TemplateDoesNotExist:
        text_template = None
        # convert HTML to text
        if html_template:
            html_text_content = html_template.render(context)
            text_content = html2markdown(html_text_content)
        else:
            text_content = ''

    msg = EmailMultiAlternatives(
        subject=subject,
        body=text_content,
        from_email=sender,
        to=to,
        bcc=bcc,
        cc=cc,
        headers=headers
    )

    if not text_only and html_content:
        msg.attach_alternative(html_content, 'text/html')
    else:
        pass

    email_attachments = htk_setting('HTK_EMAIL_ATTACHMENTS')
    if email_attachments:
        attach_images_to_message(msg, email_attachments)
        #for attachment in email_attachments:
        #    msg.attach_file(attachment)

    msg.send()


def send_markdown_email(
    subject='',
    sender=None,
    to=None,
    cc=None,
    bcc=None,
    markdown_content=''
):
    """Sends an email  w/ text and HTML produced from Markdown
    """
    sender = sender or htk_setting('HTK_DEFAULT_EMAIL_SENDER', HTK_DEFAULT_EMAIL_SENDER)
    to = to or htk_setting('HTK_DEFAULT_EMAIL_RECIPIENTS', HTK_DEFAULT_EMAIL_RECIPIENTS)
    bcc = bcc or []
    cc = cc or []

    if settings.ENV_DEV:
        subject = '[%s-dev] %s' % (htk_setting('HTK_SYMBOLIC_SITE_NAME'), subject,)

    msg = EmailMultiAlternatives(subject=subject,
                                 body=markdown_content,
                                 from_email=sender,
                                 to=to,
                                 bcc=bcc,
                                 cc=cc)

    import markdown
    html_content = markdown.markdown(markdown_content)
    msg.attach_alternative(html_content, 'text/html')

    email_attachments = htk_setting('HTK_EMAIL_ATTACHMENTS')
    if email_attachments:
        attach_images_to_message(msg, email_attachments)
        #for attachment in email_attachments:
        #    msg.attach_file(attachment)

    msg.send()
