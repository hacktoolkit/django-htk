from django import template
from django.urls import reverse

from htk.utils import htk_setting

register = template.Library()

@register.simple_tag
def redir(url, text=None, target='_blank'):
    """Links to a redirect page
    """
    redir_view = htk_setting('HTK_REDIRECT_URL_NAME')
    path = reverse(redir_view)
    text = text or url
    html = '<a href="%(path)s?url=%(url)s" target="%(target)s" title="%(url)s">%(text)s</a>' % {
        'path' : path,
        'url' : url,
        'text' : text,
        'target' : target,
    }
    return html

@register.simple_tag
def redir_trunc(url, length, target='_blank'):
    """Links to a redirect page
    """
    text = url[:length] + '...' if len(url) > length else url
    html = redir(url, text=text, target=target)
    return html
