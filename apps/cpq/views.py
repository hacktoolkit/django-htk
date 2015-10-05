from django.core.urlresolvers import reverse
from django.http import Http404
from django.shortcuts import redirect

from htk.utils.pdf_utils import render_to_pdf_response
from htk.view_helpers import render_to_response_custom as _r
from htk.view_helpers import wrap_data

def index(request):
    response = redirect('home')
    return response

def invoice(
        request,
        invoice_code,
        data=None,
        template_name='htk/fragments/cpq/invoice.html',
        renderer=_r
    ):
    if data is None:
        data = wrap_data(request)

    from htk.apps.cpq.utils import resolve_invoice_code
    invoice = resolve_invoice_code(invoice_code)
    if invoice is None:
        raise Http404
    else:
        pass

    data['invoice'] = invoice
    if request.GET.get('pdf'):
        response = render_to_pdf_response(template_name, data)
    else:
        response = renderer(template_name, data)
    return response
