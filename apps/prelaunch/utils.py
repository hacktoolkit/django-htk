# Python Standard Library Imports
import re

# Django Imports
from django.conf import settings
from django.urls import NoReverseMatch
from django.urls import reverse

# HTK Imports
from htk.apps.prelaunch.constants import *
from htk.utils import htk_setting


def get_prelaunch_url_name():
    url_name = htk_setting('HTK_PRELAUNCH_URL_NAME', HTK_PRELAUNCH_URL_NAME)
    return url_name

def get_prelaunch_uri():
    prelaunch_view_name = get_prelaunch_url_name()
    uri = reverse(prelaunch_view_name)
    return uri

def is_prelaunch_mode():
    is_prelaunch = htk_setting('HTK_PRELAUNCH_MODE', HTK_PRELAUNCH_MODE)
    if settings.TEST:
        from htk.test_scaffold.models import TestScaffold
        fake_prelaunch_mode = TestScaffold.get_fake_prelaunch_mode()
        if fake_prelaunch_mode is not None:
            is_prelaunch = fake_prelaunch_mode
    return is_prelaunch

def is_prelaunch_host(host):
    is_prelaunch = False
    prelaunch_host_regexps = htk_setting('HTK_PRELAUNCH_HOST_REGEXPS', HTK_PRELAUNCH_HOST_REGEXPS)
    for prelaunch_host_regexp in prelaunch_host_regexps:
        match = re.match(prelaunch_host_regexp, host)
        is_prelaunch = match is not None
        if is_prelaunch:
            break
    if settings.TEST:
        from htk.test_scaffold.models import TestScaffold
        fake_prelaunch_host = TestScaffold.get_fake_prelaunch_host()
        if fake_prelaunch_host is not None:
            is_prelaunch = fake_prelaunch_host
    return is_prelaunch

def is_prelaunch_exception(path):
    is_excepted = is_prelaunch_exception_url(path) or is_prelaunch_exception_view(path)
    return is_excepted

def is_prelaunch_exception_url(path):
    is_excepted = False
    prelaunch_exception_urls = htk_setting('HTK_PRELAUNCH_EXCEPTION_URLS', HTK_PRELAUNCH_EXCEPTION_URLS)
    for url in prelaunch_exception_urls:
        if re.match(url, path):
            is_excepted = True
            break
    return is_excepted

def is_prelaunch_exception_view(path):
    is_excepted = False
    prelaunch_exception_views = htk_setting('HTK_PRELAUNCH_EXCEPTION_VIEWS', HTK_PRELAUNCH_EXCEPTION_VIEWS)
    for view_name in prelaunch_exception_views:
        try:
            uri = reverse(view_name)
            if path == uri:
                is_excepted = True
                break
        except NoReverseMatch:
            pass
    return is_excepted
