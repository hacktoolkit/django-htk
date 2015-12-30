from django.http import HttpResponse

from htk.view_helpers import render_to_response_custom
from htk.utils.templates import generate_html_from_template

def render_to_pdf_response(template_name, context_dict):
    """Alias for `render_to_pdf_response_pdfkit`
    """
    response = render_to_pdf_response_pdfkit(template_name, context_dict)
    return response

def render_to_pdf_response_pdfkit(template_name, context_dict):
    """Render to a PDF response using pdfkit

    Installation: https://github.com/JazzCore/python-pdfkit/wiki/Using-wkhtmltopdf-without-X-server

    https://pypi.python.org/pypi/pdfkit
    """
    import pdfkit
    html = generate_html_from_template(template_name, context_dict)
    options = {
        'page-size' : 'Letter',
        'orientation' : 'Portrait',
        'margin-top' : '0.75in',
        'margin-bottom' : '0.75in',
        'margin-left' : '0.50in',
        'margin-right' : '0.50in',
        'encoding' : 'UTF-8',
        #'print_media_type' : False,
    }

    pdf = pdfkit.from_string(html.encode('utf-8'), False, options=options)
    if pdf:
        response = HttpResponse(pdf, content_type='application/pdf')
    else:
        response = render_to_response_custom(template_name, context_dict)
    return response

def render_to_pdf_response_pisa(template_name, context_dict):
    """Render to a PDF response using Pisa

    Caveat: xhtml2pdf / pisa seems to not be well-maintained and does not handle CSS3
    https://github.com/xhtml2pdf/xhtml2pdf/issues/44

    https://pypi.python.org/pypi/pisa/
    """
    import cStringIO as StringIO
    from xhtml2pdf import pisa
    html = generate_html_from_template(template_name, context_dict)
    result = StringIO.StringIO()
    pdf = pisa.pisaDocument(StringIO.StringIO(html.encode('utf-8')), result)
    if pdf:
        response = HttpResponse(result.getvalue(), mimetype='application/pdf')
    else:
        response = render_to_response_custom(template_name, context_dict)
    return response
