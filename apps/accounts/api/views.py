from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model
from django.views.decorators.http import require_POST

from htk.api.utils import json_response
from htk.api.utils import json_response_error
from htk.api.utils import json_response_okay
from htk.apps.accounts.utils import resolve_encrypted_uid

@login_required
def suggest(request):
    """This API endpoint supports User autocomplete

    TODO:
    First retrieve from followers and following, then search all users
    """
    UserModel = get_user_model()
    query = request.GET.get('q')
    if query:
        query = query.strip()
        user_results = UserModel.objects.filter(username__istartswith=query)
        results = [
            {
                'username' : user.username,
            }
            for user in user_results
        ]
        obj = {
            'data' : {
                'results' : results,
            },
        }
        response = json_response(obj)
    else:
        response = json_response_error()
    return response

@require_POST
@login_required
def follow(request, encrypted_uid):
    user = request.user
    other_user = resolve_encrypted_uid(encrypted_uid)
    if other_user:
        user.profile.follow_user(other_user)
        response = json_response_okay()
    else:
        response = json_response_error()
    return response

@require_POST
@login_required
def unfollow(request, encrypted_uid):
    user = request.user
    other_user = resolve_encrypted_uid(encrypted_uid)
    if other_user:
        user.profile.unfollow_user(other_user)
        response = json_response_okay()
    else:
        response = json_response_error()
    return response
