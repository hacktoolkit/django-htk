from django.contrib.sites.shortcuts import get_current_site
from django.shortcuts import redirect
from django.template.context_processors import csrf

from htk.apps.prelaunch.constants import *
from htk.apps.prelaunch.forms import PrelaunchSignupForm
from htk.apps.prelaunch.utils import is_prelaunch_mode
from htk.apps.prelaunch.view_helpers import get_view_context
from htk.utils import htk_setting
from htk.view_helpers import render_to_response_custom as _r

def prelaunch(request):
    if is_prelaunch_mode():
        data = get_view_context(request)
        data.update(csrf(request))

        success = False
        if request.method == 'POST':
            prelaunch_signup_form = PrelaunchSignupForm(request.POST)
            if prelaunch_signup_form.is_valid():
                site = get_current_site(request)
                prelaunch_signup = prelaunch_signup_form.save(site)
                success = True
            else:
                for error in prelaunch_signup_form.non_field_errors():
                    data['errors'].append(error)
        else:
            prelaunch_signup_form = PrelaunchSignupForm()
        data['prelaunch_signup_form'] = prelaunch_signup_form
        data['success'] = success
        prelaunch_template = htk_setting('HTK_PRELAUNCH_TEMPLATE', HTK_PRELAUNCH_TEMPLATE)
        response = _r(prelaunch_template, data)
    else:
        response = redirect(htk_setting('HTK_INDEX_URL_NAME'))
    return response
