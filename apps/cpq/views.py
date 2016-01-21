from django.core.urlresolvers import reverse
from django.http import Http404
from django.shortcuts import redirect
from htk.apps.cpq.decorators import cpq_admin_required
from htk.apps.cpq.enums import CPQType
from htk.utils import htk_setting
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
    """Renders an invoice, quote, or group quote
    `cpq_type` CPQType.INVOICE or CPQType.QUOTE or CPQType.GROUP_QUOTE
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

    if cpq_type in (CPQType.INVOICE, CPQType.QUOTE, CPQType.GROUP_QUOTE):
        cpq_obj_key = cpq_type.name.lower()
    else:
        raise Http404

    cpq_full_url = cpq_obj.get_full_url(base_uri=data['request']['base_uri'])
    data['cpq_type'] = cpq_obj_key
    data[cpq_obj_key] = cpq_obj
    data['%s_url' % cpq_obj_key] = cpq_full_url
    if request.GET.get('pdf'):
        data['pdf_filename'] = '%s.pdf' % cpq_obj_key
        from htk.utils.pdf_utils import render_to_pdf_response
        response = render_to_pdf_response(template_name, data, show_content_in_browser=False)
    else:
        response = renderer(template_name, data)
    return response

def groupquote(request, quote_code):
    template_name = htk_setting('HTK_CPQ_TEMPLATE_NAME_GROUP_QUOTE')
    response = cpq_view(request, quote_code, CPQType.GROUP_QUOTE, template_name)
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
    from htk.apps.cpq.utils.general import get_admin_urls
    from htk.apps.cpq.utils.general import get_reporting_urls
    from htk.apps.cpq.utils.general import get_tools_urls
    data = wrap_data(request)
    data['admin_urls'] = get_admin_urls()
    data['reporting_urls'] = get_reporting_urls()
    data['tools_urls'] = get_tools_urls()
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

@cpq_admin_required
def import_customers(request):
    renderer = get_renderer()
    wrap_data = get_template_context_generator()
    data = wrap_data(request)
    from htk.apps.customers.forms import OrganizationCustomersImportForm
    success = False
    if request.method == 'POST':
        data['was_submitted'] = True
        import_customers_form = OrganizationCustomersImportForm(request.POST, request.FILES)
        if import_customers_form.is_valid():
            customers = import_customers_form.save()
            data['organization_customer'] = import_customers_form.organization_customer
            data['customers'] = customers
            success = True
        else:
            customers = None
    else:
        import_customers_form = OrganizationCustomersImportForm()

    data['import_customers_form'] = import_customers_form
    data['success'] = success
    template_name = htk_setting('HTK_CPQ_TEMPLATE_NAME_IMPORT_CUSTOMERS')
    response = renderer(template_name, data)
    return response
