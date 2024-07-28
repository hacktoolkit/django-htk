# Python Standard Library Imports
import itertools
import re

# Django Imports
from django.conf import settings
from django.urls import (
    NoReverseMatch,
    reverse,
)

# HTK Imports
from htk.utils import htk_setting


# isort: off


def get_prelaunch_url_name():
    url_name = htk_setting('HTK_PRELAUNCH_URL_NAME')
    return url_name


def get_prelaunch_uri():
    prelaunch_view_name = get_prelaunch_url_name()
    uri = reverse(prelaunch_view_name)
    return uri


def is_prelaunch_mode():
    is_prelaunch = htk_setting('HTK_PRELAUNCH_MODE')
    if settings.TEST:
        from htk.test_scaffold.models import TestScaffold

        fake_prelaunch_mode = TestScaffold.get_fake_prelaunch_mode()
        if fake_prelaunch_mode is not None:
            is_prelaunch = fake_prelaunch_mode
    return is_prelaunch


def is_prelaunch_host(host):
    is_prelaunch = False
    prelaunch_host_regexps = htk_setting('HTK_PRELAUNCH_HOST_REGEXPS')
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
    is_excepted = is_prelaunch_exception_url(
        path
    ) or is_prelaunch_exception_view(path)
    return is_excepted


def is_prelaunch_exception_url(path):
    is_excepted = False
    prelaunch_exception_urls = htk_setting('HTK_PRELAUNCH_EXCEPTION_URLS')
    for url in prelaunch_exception_urls:
        if re.match(url, path):
            is_excepted = True
            break
    return is_excepted


def is_prelaunch_exception_view(path):
    """Determines if the path is an excepted view from prelaunch redirection

    This solution is non-ideal because it reverses the view name from a list of view names, which is
    not always possible because we do not always have the args and kwargs necessary to reverse the view name.

    A preferred approach would be to take as a parameter the `request` object, and check if the view name matches
    the `request.resolver_match` object. However, this is not possible because the middleware does not have access
    at this point -- the request has not yet been resolved to a view.
    """
    is_excepted = False
    prelaunch_exception_views = htk_setting('HTK_PRELAUNCH_EXCEPTION_VIEWS')
    for view_name in prelaunch_exception_views:
        try:
            uri = reverse(view_name)
            if path == uri:
                is_excepted = True
                break
        except NoReverseMatch:
            pass
    return is_excepted


def get_early_access_code(request):
    key = 'early_access_code'
    header = 'X-HTK-Early-Access-Code'
    early_access_code = (
        request.GET.get(key)
        or request.COOKIES.get(key)
        or request.session.get(key)
        or request.headers.get(header)
    )
    return early_access_code


def has_early_access(request, early_access_code=None):
    from htk.apps.prelaunch.loading import PrelaunchSignup

    has_access = False

    if early_access_code is None:
        early_access_code = get_early_access_code(request)

    if early_access_code:
        try:
            prelaunch_signup = PrelaunchSignup.objects.get(
                early_access_code=early_access_code
            )
            has_access = prelaunch_signup.early_access
        except PrelaunchSignup.DoesNotExist:
            prelaunch_signup = None

    return has_access


def get_unique_signups():
    """Returns a list of PrelaunchSignup objects with unique emails,
    as some users may sign up multiple times.
    """
    from htk.apps.prelaunch.loading import PrelaunchSignup

    q = PrelaunchSignup.objects.order_by('email', 'id')
    prelaunch_signups = [
        list(g)[0]
        for (
            email,
            g,
        ) in itertools.groupby(q, lambda _: _.email)
    ]
    return prelaunch_signups
