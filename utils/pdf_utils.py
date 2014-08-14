import cStringIO as StringIO
from xhtml2pdf import pisa

from django.http import HttpResponse
from django.template import Context
from django.template import TemplateDoesNotExist
from django.template import loader

from htk.view_helpers import render_to_response_custom

def render_to_pdf_response(template_name, context_dict):
    try:
        template = loader.get_template(template_name)
        context = Context(context_dict)
        html = template.render(context)
    except TemplateDoesNotExist:
        html = ''
    result = StringIO.StringIO()
    pdf = pisa.pisaDocument(StringIO.StringIO(html.encode('utf-8')), result)
    if not pdf.err:
        response = HttpResponse(result.getvalue(), mimetype='application/pdf')
    else:
        response = render_to_response_custom(template_name, context_dict)
    return response
