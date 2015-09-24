from django.shortcuts import redirect
from django.core.urlresolvers import reverse

from htk.apps.maintenance_mode.utils import is_maintenance_mode
from htk.utils import htk_setting

class MaintenanceModeMiddleware(object):
    """Checks whether HTK_MAINTENANCE_MODE is set

    If so, redirects to the HTK_MAINTENANCE_MODE_URL_NAME page
    """
    def process_request(self, request):
        maintenance_mode_page = reverse(htk_setting('HTK_MAINTENANCE_MODE_URL_NAME'))
        response = None
        if request.path == maintenance_mode_page:
            if not is_maintenance_mode():
                response = redirect('/')
            else:
                # already here
                pass
        else:
            if is_maintenance_mode():
                response = redirect(maintenance_mode_page)
            else:
                pass
        return response
