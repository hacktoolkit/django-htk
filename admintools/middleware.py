import rollbar

class HtkEmulateUserMiddleware(object):
    def _can_emulate_another_user(self, request):
        can_emulate = False
        if request.user.is_authenticated():
            try:
                user_profile = request.user.profile
                if user_profile.is_company_officer:
                    can_emulate = True
            except:
                rollbar.report_exc_info(request=request)
        return can_emulate

    def process_request(self, request):
        if self._can_emulate_another_user(request):
            from htk.apps.accounts.utils import get_user_by_id
            from htk.apps.accounts.utils import get_user_by_username
            user_id = request.COOKIES.get('emulate_user_id')
            username = request.COOKIES.get('emulate_user_username')
            if user_id or username:
                if user_id:
                    emulated_user = get_user_by_id(user_id)
                elif username:
                    emulated_user = get_user_by_username(username)
                if emulated_user and not emulated_user.profile.is_company_officer:
                    request.original_user = request.user
                    request.user = emulated_user

    def process_response(self, request, response):
        if self._can_emulate_another_user(request):
            response.delete_cookie('emulate_user_id')
            response.delete_cookie('emulate_user_username')
        return response
