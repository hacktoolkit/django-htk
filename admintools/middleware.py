from htk.admintools.utils import can_emulate_another_user
from htk.admintools.utils import can_emulate_user

class HtkEmulateUserMiddleware(object):
    def process_request(self, request):
        if can_emulate_another_user(request.user):
            from htk.apps.accounts.utils import get_user_by_id
            from htk.apps.accounts.utils import get_user_by_username
            user_id = request.COOKIES.get('emulate_user_id')
            username = request.COOKIES.get('emulate_user_username')
            if user_id or username:
                if user_id:
                    emulated_user = get_user_by_id(user_id)
                elif username:
                    emulated_user = get_user_by_username(username)
                if can_emulate_user(request.user, emulated_user):
                    request.original_user = request.user
                    request.user = emulated_user

    def process_response(self, request, response):
        if can_emulate_another_user(request.user):
            response.delete_cookie('emulate_user_id')
            response.delete_cookie('emulate_user_username')
        return response
