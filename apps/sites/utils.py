# Python Standard Library Importsp
import re

# Third Party / PIP Imports

# Django Imports

# HTK Imports
from htk.utils import htk_setting
from htk.utils.request import get_current_request


def get_current_site(request=None):
    """Returns the current site if a Request object is available

    Improves upon django.contrib.sites.shortcuts.get_current_site by also allowing subdomains
    """
    if request is None:
        request = get_current_request()

    site = None

    if request:
        from django.contrib.sites.models import Site

        hostname = request.get_host()

        for _site in Site.objects.all():
            # TODO: expensive, cache
            domain = _site.domain
            domain_regex = r'^(?:.*\.)?%s$' % domain.replace('.', '\.')
            if re.match(domain_regex, hostname):
                site = _site
                break
    else:
        pass

    return site


def get_site_name(request=None):
    """Returns the current site name
    """
    site = get_current_site(request=request)
    site_name = site.name if site else None

    if not site_name:
        site_name = htk_setting('HTK_SITE_NAME')

    return site_name
