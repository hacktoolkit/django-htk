# Third Party (PyPI) Imports
import rollbar

# Django Imports
from django.shortcuts import redirect

# HTK Imports
from htk.apps.url_shortener.utils import resolve_short_url_code
from htk.utils import htk_setting


def short_url(request, code):
    host = request.get_host()
    short_url = resolve_short_url_code(host, code)
    if short_url:
        try:
            short_url.record_request(request)
        except:
            rollbar.report_exc_info(request=request)
        url = short_url.url
        response = redirect(url)
    else:
        default_url = 'http://%s' % htk_setting('HTK_CANONICAL_DOMAIN')
        response = redirect(default_url)
    return response
