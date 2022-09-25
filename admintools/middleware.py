# Python Standard Library Imports

# Third Party (PyPI) Imports
import rollbar

# Django Imports
from django.contrib import messages
from django.utils.deprecation import MiddlewareMixin

# HTK Imports
from htk.admintools.utils import (
    is_allowed_to_emulate,
    is_allowed_to_emulate_users,
    request_emulate_user,
)
from htk.utils import htk_setting


class HtkEmulateUserMiddleware(MiddlewareMixin):
    def process_request(self, request):
        """Replace the authenticated `request.user` if properly emulating"""
        if request.path.startswith(
            htk_setting('HTK_PATH_ADMIN')
        ) or request.path.startswith(htk_setting('HTK_PATH_ADMINTOOLS')):
            # disallow emulation for /admin and /admintools
            pass
        else:
            user_id = request.COOKIES.get('emulate_user_id')
            username = request.COOKIES.get('emulate_user_username')
            request_emulate_user(request, user_id=user_id, username=username)

    def process_response(self, request, response):
        """Delete user emulation cookies if they should not be set"""
        original_user = getattr(request, 'original_user', None)
        user = getattr(request, 'user', None)
        is_emulating = original_user is not None and user is not None
        if not is_emulating:
            response.delete_cookie('emulate_user_id')
            response.delete_cookie('emulate_user_username')

        return response
