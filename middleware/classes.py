# Third Party (PyPI) Imports
from user_agents import parse

# Python Standard Library Imports
import re
import sys

# Django Imports
from django.shortcuts import redirect
from django.utils import timezone
from django.utils.deprecation import MiddlewareMixin

# HTK Imports
from htk.utils import htk_setting
from htk.utils.http.errors import HttpErrorResponseError
from htk.utils.request import is_allowed_host


is_py2 = sys.version[0] == '2'
if is_py2:
    import thread as _thread
else:
    import _thread


class GlobalRequestMiddleware(MiddlewareMixin):
    """Stores the request object so that it is accessible globally

    Makes an assumption that one request runs entirely in one thread
    If a request happens to spin off other threads, I suppose the request object would not be accessible
    """
    _threadmap = {}

    @classmethod
    def get_current_request(cls):
        request = cls._threadmap.get(_thread.get_ident())
        return request

    def process_request(self, request):
        self._threadmap[_thread.get_ident()] = request

    def process_exception(self, request, exception):
        try:
            del self._threadmap[_thread.get_ident()]
        except KeyError:
            pass

    def process_response(self, request, response):
        try:
            del self._threadmap[_thread.get_ident()]
        except KeyError:
            pass
        return response


class AllowedHostsMiddleware(MiddlewareMixin):
    """Checks that host is inside ALLOWED_HOST_REGEXPS

    If not, will redirect to HTK_DEFAULT_DOMAIN

    If host ends with '.', will redirect to host with '.' stripped
    """
    def process_request(self, request):
        host = request.get_host()
        request_path = request.path
        redirect_uri = None
        https_prefix = 's' if request.is_secure() else ''
        if request_path == '/health_check':
            return False
        elif not is_allowed_host(host):
            redirect_uri = 'http%s://%s%s' % (https_prefix, htk_setting('HTK_DEFAULT_DOMAIN'), request_path,)
        elif len(host) > 1 and host[-1] == '.':
            redirect_uri = 'http%s://%s%s' % (https_prefix, host[:-1], request_path,)

        if redirect_uri:
            return redirect(redirect_uri)


class RequestTimerMiddleware(MiddlewareMixin):
    """Timer to observe how long a request takes to process
    """
    _threadmap = {}

    @classmethod
    def get_current_timer(cls):
        timer = cls._threadmap.get(_thread.get_ident())
        return timer

    def __init__(self, *args, **kwargs):
        super(RequestTimerMiddleware, self).__init__(*args, **kwargs)

        from htk.utils.timer import HtkTimer
        timer = HtkTimer()
        timer.start()
        self.timer = timer

    def process_request(self, request):
        timer = self.timer
        self._threadmap[_thread.get_ident()] = timer


class RewriteJsonResponseContentTypeMiddleware(MiddlewareMixin):
    """This middleware exists because IE is a stupid browser and tries to
    download application/json content type from XHR responses as file
    """
    def process_response(self, request, response):
        if self._is_response_json(response) and self._is_user_agent_msie(request):
            response['Content-Type'] = 'text/plain'
        return response

    def _is_response_json(self, response):
        is_json = response.get('Content-Type', '') == 'application/json'
        return is_json

    def _is_user_agent_msie(self, request):
        user_agent = request.META.get('HTTP_USER_AGENT', '')
        is_msie = bool(re.match('.*MSIE.*', user_agent))
        return is_msie


class TimezoneMiddleware(MiddlewareMixin):
    def process_request(self, request):
        # django_timezone = request.session.get(DJANGO_TIMEZONE, None)
        # if not django_timezone and request.user.is_authenticated:
        if request.user.is_authenticated:
            user = request.user
            django_timezone = user.profile.get_django_timezone()
            # <DstTzInfo 'America/Los_Angeles' PST-1 day, 16:00:00 STD> is not JSON serializable
            # request.session[DJANGO_TIMEZONE] = django_timezone
        else:
            django_timezone = None
        if django_timezone:
            timezone.activate(django_timezone)


class HttpErrorResponseMiddleware:
    """This middleware allows `HttpErrorResponseError`s to be thrown
    to short-circuit processing of a view, and allows a response to be returned
    instead.
    """

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        return response

    def process_exception(self, request, exception):
        if isinstance(exception, HttpErrorResponseError):
            response = exception.response
        else:
            response = None

        return response

class UserAgentMiddleware:
    """Middleware to parse the user agent and add it to the request object."""
    def __init__(self, get_response=None):
        if get_response is not None:
            self.get_response = get_response

    def __call__(self, request):
        # Code to be executed for each request before
        # the view (and later middleware) are called.
        request = self.process_request(request)
        response = self.get_response(request)
        return response

    def process_request(self, request):
        user_agent = parse(request.META.get('HTTP_USER_AGENT', ''))
        request.user_agent = user_agent
        return request
