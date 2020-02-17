# Django Imports
from django.views.decorators.http import require_POST

# HTK Imports
from htk.api.utils import json_response_error
from htk.api.utils import json_response_okay
from htk.apps.notifications.utils import dismiss_alert_for_user


@require_POST
def dismiss_alert(request):
    user = request.user
    success = False
    if request.user.is_authenticated:
        alert_name = request.POST.get('alert_name')
        success = dismiss_alert_for_user(user, alert_name)

    response = json_response_okay() if success else json_response_error()
    return response
