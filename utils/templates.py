from htk.utils import htk_setting
from htk.utils import resolve_method_dynamically

def get_renderer():
    renderer = resolve_method_dynamically(htk_setting('HTK_TEMPLATE_RENDERER'))
    return renderer

def get_template_context_generator():
    wrap_data = resolve_method_dynamically(htk_setting('HTK_TEMPLATE_CONTEXT_GENERATOR'))
    return wrap_data

def generate_html_from_template(template_name, context_dict):
    """Generate HTML by using `template_name` inflated with `context_dict`
    """
    from django.template import Context
    from django.template import TemplateDoesNotExist
    from django.template import loader
    try:
        template = loader.get_template(template_name)
        context = Context(context_dict)
        html = template.render(context)
    except TemplateDoesNotExist:
        html = ''
    return html
