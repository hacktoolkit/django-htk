import base64

from django import template
from django.urls import reverse
from django.utils.safestring import mark_safe

from htk.utils import htk_setting

register = template.Library()

@register.simple_tag
def redir_url(url):
    redir_view = htk_setting('HTK_REDIRECT_URL_NAME')
    url = '%(path)s?url=%(url)s' % {
        'path' : reverse(redir_view),
        'url' : base64.urlsafe_b64encode(url.encode()).decode(),
    }
    return url

@register.simple_tag
def redir(url, text=None, target='_blank'):
    """Links to a redirect page
    """
    text = text or url
    html = '<a href="%(url)s" target="%(target)s">%(text)s</a>' % {
        'url' : redir_url(url),
        'text' : text,
        'target' : target,
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
