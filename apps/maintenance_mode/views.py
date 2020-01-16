# HTK Imports
from htk.utils import htk_setting


def maintenance_mode(request):
    from htk.views import generic_template_view
    template_name = 'maintenance_mode.html'
    response = generic_template_view(request, template_name)
    return response
