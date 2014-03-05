from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model

from htk.api.utils import json_response
from htk.api.utils import json_response_error
from htk.api.utils import json_response_okay

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
