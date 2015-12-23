from django.core.urlresolvers import reverse
from django.http import Http404
from django.shortcuts import redirect
from htk.apps.cpq.decorators import cpq_admin_required
from htk.apps.cpq.enums import CPQType
from htk.utils import htk_setting
from htk.utils.pdf_utils import render_to_pdf_response
from htk.utils.templates import get_renderer
from htk.utils.templates import get_template_context_generator
from htk.view_helpers import render_to_response_custom as _r
from htk.view_helpers import wrap_data as htk_wrap_data

def index(request):
    data = htk_wrap_data(request)
    user = data['user']
    if user and user.is_staff:
        response = redirect('cpq_dashboard')
    else:
        response = redirect('index')
    return response

##
# public views

def cpq_view(request, cpq_code, cpq_type, template_name):
    """Renders an invoice or a quote
    `cpq_type` CPQType.INVOICE or CPQType.QUOTE
    """
    renderer = get_renderer()
    wrap_data = get_template_context_generator()
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

def invoice(request, invoice_code):
    template_name = htk_setting('HTK_CPQ_TEMPLATE_NAME_INVOICE')
    response = cpq_view(request, invoice_code, CPQType.INVOICE, template_name)
    return response

def quote(request, quote_code):
    template_name = htk_setting('HTK_CPQ_TEMPLATE_NAME_QUOTE')
    response = cpq_view(request, quote_code, CPQType.QUOTE, template_name)
    return response

##
# admin views
@cpq_admin_required
def dashboard(request):
    renderer = get_renderer()
    wrap_data = get_template_context_generator()
    data = wrap_data(request)
    template_name = htk_setting('HTK_CPQ_TEMPLATE_NAME_DASHBOARD')
    response = renderer(template_name, data)
    return response

@cpq_admin_required
def receivables(request, year=None):
    renderer = get_renderer()
    wrap_data = get_template_context_generator()
    data = wrap_data(request)
    from htk.apps.cpq.utils import get_invoice_years
    data['invoice_years'] = get_invoice_years()
    if year:
        from htk.apps.cpq.utils import get_receivables_by_year
        receivables = get_receivables_by_year(year)
        if receivables.exists():
            data['invoice_year'] = year
            data['receivables'] = receivables
            data['total'] = sum([invoice.get_total() for invoice in receivables])
    template_name = htk_setting('HTK_CPQ_TEMPLATE_NAME_RECEIVABLES')
    response = renderer(template_name, data)
    return response
