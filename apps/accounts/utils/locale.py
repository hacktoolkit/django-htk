# HTK Imports
from htk.utils.request import get_current_request


def get_local_time(dt=None, user=None):
    if user is None:
        request = get_current_request()
        user = request.user if request and hasattr(request, 'user') and request.user.is_authenticated else None

    if user:
        local_time = user.profile.get_local_time(dt=dt)
    else:
        local_time = dt

    return local_time
