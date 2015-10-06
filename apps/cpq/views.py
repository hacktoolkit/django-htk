from django.core.urlresolvers import reverse
from django.http import Http404
from django.shortcuts import redirect

from htk.apps.cpq.enums import CPQType
from htk.utils.pdf_utils import render_to_pdf_response
from htk.view_helpers import render_to_response_custom as _r
from htk.view_helpers import wrap_data

def index(request):
    response = redirect('home')
    return response

def cpq_view(
        request,
        cpq_code,
        cpq_type, # CPQType.INVOICE or CPQType.QUOTE
        data=None,
        template_name='htk/fragments/cpq/invoice.html',
        renderer=_r
    ):
    if data is None:
        data = wrap_data(request)

    from htk.apps.cpq.enums import CPQType
    from htk.apps.cpq.utils import resolve_cpq_code
    cpq_obj = resolve_cpq_code(cpq_code, cpq_type=cpq_type)
    if cpq_obj is None:
        raise Http404
    else:
        pass

    if cpq_type == CPQType.INVOICE:
        data_key = 'invoice'
    elif cpq_type == CPQType.QUOTE:
        data_key = 'quote'
    else:
        raise Http404

    data[data_key] = cpq_obj
    if request.GET.get('pdf'):
        response = render_to_pdf_response(template_name, data)
    else:
        response = renderer(template_name, data)
    return response

def invoice(
        request,
        invoice_code,
        data=None,
        template_name='htk/fragments/cpq/invoice.html',
        renderer=_r
    ):
    response = cpq_view(
        request,
        invoice_code,
        cpq_type=CPQType.INVOICE,
        data=data,
        template_name=template_name,
        renderer=renderer
    )
    return response

def quote(
        request,
        quote_code,
        data=None,
        template_name='htk/fragments/cpq/quote.html',
        renderer=_r
    ):
    response = cpq_view(
        request,
        quote_code,
        cpq_type=CPQType.QUOTE,
        data=data,
        template_name=template_name,
        renderer=renderer
    )
    return response
