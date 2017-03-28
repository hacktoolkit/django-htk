from django.shortcuts import redirect

from htk.apps.accounts.constants import *
from htk.apps.accounts.session_keys import *

def get_social_auths_status(user):
    user_social_auths = user.profile.get_social_auths()
    status_dict = {}
    for social_auth in user_social_auths:
        status_dict[social_auth.provider] = True

    status_list = []
    for social_auth in SOCIAL_AUTHS:
        key = social_auth['key']
        name = social_auth['name']
        item = {
            'key' : key,
            'name' : name,
            'linked' : status_dict.get(key, False)
        }
        status_list.append(item)
    return status_list

def redirect_to_social_auth_complete(request):
    """Return an HTTP Redirect response to social:complete to continue the pipeline
    """
    backend = request.session['backend']
    #backend = request.session[SOCIAL_AUTH_PARTIAL_PIPELINE_KEY]['backend']
    response = redirect('social:complete', backend=backend)
    return response
