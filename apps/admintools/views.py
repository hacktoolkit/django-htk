# HTK Imports
from htk.view_helpers import render_custom as _r
from htk.utils import htk_setting
from htk.admintools.decorators import company_employee_required
from htk.api.utils import json_response_okay
from htk.apps.admintools.utils import build_admintools_paths


@company_employee_required
def admintools_view(request, *args):
    data = {
        'is_react_dev_mode': True,
        'vite_dev_url': htk_setting('HTK_ADMINTOOLS_VITE_URL'),
    }
    response = _r(request, 'htk/admintools/app.html', data=data)
    return response


@company_employee_required
def app_config(request, *args, **kwargs):
    response = json_response_okay(
        {
            'paths': build_admintools_paths(),
        }
    )
    return response
