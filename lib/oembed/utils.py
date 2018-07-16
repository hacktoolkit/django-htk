import re
import requests
import rollbar
import urllib

from htk.lib.oembed.cachekeys import OembedResponseCache
from htk.lib.oembed.constants import *
from htk.utils.request import get_current_request

def get_oembed_html(url, autoplay=False):
    """Gets the oEmbed HTML for a URL, if it is an oEmbed type
    """
    oembed_type = get_oembed_type(url)

    if oembed_type:
        if oembed_type == 'youtube':
            html = youtube_oembed(url, autoplay=autoplay)
        else:
            html = get_oembed_html_for_service(url, oembed_type)
    else:
        html = None
    return html

def get_oembed_html_for_service(url, service):
    """Returns the oEmbed HTML for `service` (YouTube, Vimeo, etc)

    Makes an HTTP request, so we should probably cache its response
    """
    c = OembedResponseCache(prekey=url)
    html = c.get()
    if html is None:
        request = None
        success = False
        try:
            oembed_base_url = OEMBED_BASE_URLS[service]
            oembed_url = oembed_base_url % {
                'url' : urllib.quote(url),
            }
            response = requests.get(oembed_url)
            if response.status_code >= 400:
                pass
            else:
                data = response.json()
                html = data['html']
                c.cache_store(html)
                success = True
        except:
            request = get_current_request()
            extra_data = {
                'message' : 'Bad oembed URL',
                'oembed_url' : oembed_url,
                'url' : url,
                'response' : {
                    'status_code' : response.status_code,
                    'content' : response.content,
                }
            }
            rollbar.report_exc_info(level='warning', request=request, extra_data=extra_data)

        if success:
            pass
        else:
            html = '<a href="%(url)s" target="_blank">%(url)s</a>' % {
                'url' : url,
            }
    else:
        pass
    return html

def get_oembed_type(url):
    """Determines the type of oEmbed this URL is, if it exists
    """
    oembed_type = None
    for service, pattern in OEMBED_URL_SCHEME_REGEXPS.iteritems():
        if re.match(pattern, url, flags=re.I):
            oembed_type = service
            break
    return oembed_type

def youtube_oembed(url, autoplay=False):
    html = get_oembed_html_for_service(url, 'youtube')
    if autoplay:
        replacement = '?feature=oembed&autoplay=1&rel=0&modestbranding=1'
    else:
        replacement = '?feature=oembed&rel=0&modestbranding=1'
    html = re.sub(
        r'\?feature=oembed',
        replacement,
        html
    )
    return html

def youtube_oembed_autoplay(url):
    html = youtube_oembed(url, autoplay=True)
    return html
