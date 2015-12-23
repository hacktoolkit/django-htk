from htk.utils import htk_setting
from htk.utils import resolve_method_dynamically

def get_renderer():
    renderer = resolve_method_dynamically(htk_setting('HTK_TEMPLATE_RENDERER'))
    return renderer

def get_template_context_generator():
    wrap_data = resolve_method_dynamically(htk_setting('HTK_TEMPLATE_CONTEXT_GENERATOR'))
    return wrap_data
