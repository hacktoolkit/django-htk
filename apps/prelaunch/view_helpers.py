# HTK Imports
from htk.utils import htk_setting
from htk.utils.general import resolve_method_dynamically


def get_view_context(request):
    view_context_generator = htk_setting('HTK_PRELAUNCH_VIEW_CONTEXT_GENERATOR', '')
    method = resolve_method_dynamically(view_context_generator)
    if method:
        context = method(request)
    else:
        context = {}
    return context
