# Django Imports
from django import template
from django.urls import reverse
from django.utils.safestring import mark_safe

# HTK Imports
from htk.compat import b64encode
from htk.utils import htk_setting


register = template.Library()


@register.simple_tag
def redir_url(url):
    redir_view = htk_setting('HTK_REDIRECT_URL_NAME')

    encoded_url = b64encode(url, url_safe=True)

    url = '%(path)s?url=%(url)s' % {
        'path': reverse(redir_view),
        'url': encoded_url
    }
    return url


@register.simple_tag
def redir(url, text=None, target='_blank'):
    """Links to a redirect page
    """
    text = text or url
    html = '<a href="%(url)s" target="%(target)s">%(text)s</a>' % {
        'url': redir_url(url),
        'text': text,
        'target': target,
    }
    html = mark_safe(html)
    return html


@register.simple_tag
def redir_trunc(url, length, target='_blank'):
    """Links to a redirect page
    """
    text = url[:length] + '...' if len(url) > length else url
    html = redir(url, text=text, target=target)
    return html
