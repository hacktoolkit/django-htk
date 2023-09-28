# HTK Imports
from htk.view_helpers import render_custom as _r
from htk.utils import htk_setting


def admintools_view(request, *args):
    data = {
        'is_react_dev_mode': True,
        'vite_dev_url': htk_setting('HTK_ADMINTOOLS_VITE_URL'),
    }
    response = _r(request, 'htk/admintools/app.html', data=data)
    return response
