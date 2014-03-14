import re
import requests
import rollbar
import urllib

from htk.lib.oembed.cachekeys import OembedResponseCache
from htk.lib.oembed.constants import *
from htk.middleware import GlobalRequestMiddleware

def get_oembed_html(url):
    """Gets the oEmbed HTML for a URL, if it is an oEmbed type
    """
    oembed_type = get_oembed_type(url)
    if oembed_type:
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
            oembed_url = oembed_base_url % urllib.quote(url)
            response = requests.get(oembed_url)
            if response.status_code >= 400:
                pass
            else:
                data = response.json()
                html = data['html']
                c.cache_store(html)
                success = True
        except:
            request = GlobalRequestMiddleware.get_current_request()
            rollbar.report_exc_info(request=request)

        if success:
            pass
        else:
            html = 'Failed to get oEmbed for URL: %s' % url
            if request is None:
                request = GlobalRequestMiddleware.get_current_request()
            else:
                pass
            rollbar.report_message('Bad oembed url <%s>' % (url), 'warning', request)
    else:
        pass
    return html

def get_oembed_type(url):
    """Determines the type of oEmbed this URL is, if it exists
    """
    oembed_type = None
    if re.match(SLIDESHARE_URL_REGEXP, url, flags=re.I):
        oembed_type = 'slideshare'
    elif re.match(VIMEO_URL_REGEXP, url, flags=re.I):
        oembed_type = 'vimeo'
    elif re.match(YOUTUBE_URL_REGEXP, url, flags=re.I):
        oembed_type = 'youtube'
    else:
        pass
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
