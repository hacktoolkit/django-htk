from django.template.base import Library
from django.template.defaultfilters import stringfilter

register = Library()

@register.filter(is_safe=True)
def concat(value, arg):
    result = str(value) + str(arg)
    return result

@register.simple_tag(takes_context=True)
def lesscss(context, css_file_path_base):
    values = {
        'css_rel' : context.get('css_rel', 'stylesheet'),
        'css_ext' : context.get('css_ext', 'css'),
        'css_file_path_base' : css_file_path_base,
    }
    html = '<link type="text/css" rel="%(css_rel)s" href="%(css_file_path_base)s.%(css_ext)s" />' % values
    return html

@register.simple_tag(takes_context=True)
def loadjs(context, js_file_path):
    asset_version = context.get('asset_version')
    if asset_version:
        asset_version_str = '?v=%s' % asset_version
    else:
        asset_version_str = ''
    values = {
        'js_file_path' : js_file_path,
        'asset_version_str' : asset_version_str,
    }
    html = '<script type="text/javascript" src="%(js_file_path)s%(asset_version_str)s"></script>' % values
    return html
