# Python Standard Library Imports

# Django Imports
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.utils.deprecation import MiddlewareMixin

# HTK Imports
from htk.apps.maintenance_mode.utils import is_maintenance_mode
from htk.utils import htk_setting


class MaintenanceModeMiddleware(MiddlewareMixin):
    """Checks whether HTK_MAINTENANCE_MODE is set

    If so, redirects to the HTK_MAINTENANCE_MODE_URL_NAME page
    """
    def process_request(self, request):
        namespace = htk_setting('HTK_URLS_NAMESPACE')
        url_name_suffix = htk_setting('HTK_MAINTENANCE_MODE_URL_NAME')
        if namespace:
            url_name = '%s:%s' % (namespace, url_name_suffix,)
        else:
            url_name = url_name_suffix
        maintenance_mode_page = reverse_lazy(url_name)
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
