# HTK Imports
from htk.utils.request import get_current_request


def get_authenticated_user():
    """Returns the currently authenticated user, or None
    """
    request = get_current_request()
    if request and hasattr(request, 'user') and request.user.is_authenticated:
        user = request.user
    else:
        user = None
    return user
