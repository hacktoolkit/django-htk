# HTK Imports
from htk.utils import htk_setting
from htk.view_helpers import render_custom as _r
from htk.view_helpers import wrap_data


def changelog_view(request, template, data=None, renderer=_r):
    if data is None:
        data = wrap_data(request)

    filename = htk_setting('HTK_CHANGELOG_FILE_PATH')
    with open(filename, 'r') as f:
        changelog = f.read()

    data['changelog'] = changelog

    response = renderer(request, template, data)
    return response
