# Django Imports
from django.shortcuts import redirect
from django.utils.deprecation import MiddlewareMixin

# HTK Imports
from htk.apps.prelaunch.utils import (
    get_prelaunch_uri,
    is_prelaunch_exception,
    is_prelaunch_host,
    is_prelaunch_mode,
)


class PrelaunchModeMiddleware(MiddlewareMixin):
    def process_request(self, request):
        host = request.get_host()
        path = request.path

        if is_prelaunch_mode() and not is_prelaunch_host(host) and not is_prelaunch_exception(path):
            prelaunch_uri = get_prelaunch_uri()
            return redirect(prelaunch_uri)
