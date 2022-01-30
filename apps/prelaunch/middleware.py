# Django Imports
from django.shortcuts import redirect
from django.utils.deprecation import MiddlewareMixin

# HTK Imports
from htk.apps.prelaunch.utils import (
    get_early_access_code,
    get_prelaunch_uri,
    has_early_access,
    is_prelaunch_exception,
    is_prelaunch_host,
    is_prelaunch_mode,
)


class PrelaunchModeMiddleware(MiddlewareMixin):
    def __init__(self, *args, **kwargs):
        super(PrelaunchModeMiddleware, self).__init__(*args, **kwargs)
        self.has_early_access = False
        self.early_access_code = None

    def process_request(self, request):
        host = request.get_host()
        path = request.path

        self.early_access_code = get_early_access_code(request)
        self.has_early_access = has_early_access(request, early_access_code=self.early_access_code)

        should_redirect_to_prelaunch = (
            is_prelaunch_mode()
            and not self.has_early_access
            and not is_prelaunch_host(host)
            and not is_prelaunch_exception(path)
        )

        if should_redirect_to_prelaunch:
            prelaunch_uri = get_prelaunch_uri()
            return redirect(prelaunch_uri)

    def process_response(self, request, response):
        if self.has_early_access:
            request.session['early_access_code'] = self.early_access_code
            response.set_cookie('early_access_code', self.early_access_code)

        return response
