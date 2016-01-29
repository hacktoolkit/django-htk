from django.core.urlresolvers import reverse
from django.http import Http404
from django.shortcuts import redirect
from django.views.decorators.http import require_POST

from htk.api.utils import json_response_error
from htk.api.utils import json_response_okay
from htk.apps.cpq.decorators import cpq_admin_required
from htk.apps.cpq.enums import CPQType
from htk.lib.stripe_lib.utils import get_stripe_public_key
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
    if htk_setting('HTK_CPQ_PAY_ONLINE'):
        live_mode = htk_setting('HTK_STRIPE_LIVE_MODE')
        data['stripe_key'] = get_stripe_public_key(live_mode=live_mode)
        data['cpq_payment_uri'] = cpq_obj.get_payment_uri()
    data['cpq_obj'] = cpq_obj
    data['cpq_url'] = cpq_full_url
    # deprecated
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

def groupquote_all(request, quote_code):
    template_name = htk_setting('HTK_CPQ_TEMPLATE_NAME_GROUP_QUOTE_ALL')
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

@require_POST
def cpq_pay(request, cpq_code, cpq_type):
    from htk.apps.cpq.utils import resolve_cpq_code
    cpq_obj = resolve_cpq_code(cpq_code, cpq_type=cpq_type)
    if cpq_obj is None:
        raise Http404
    if not htk_setting('HTK_CPQ_PAY_ONLINE'):
        raise Http404

    success = False
    try:
        stripe_token = request.POST.get('stripeToken')
        amount = int(request.POST.get('amount'))
        email = request.POST.get('email')
        line_item_ids = request.POST.get('lineItemIds').split(',')
        success = cpq_obj.approve_and_pay(stripe_token, amount, email, line_item_ids)
    except ValueError:
        # most likely encountered exception parsing `amount` or `line_item_ids`
        pass

    if success:
        response = json_response_okay()
    else:
        response = json_response_error()
    return response

@require_POST
def quote_pay(request, quote_code):
    return cpq_pay(request, quote_code, CPQType.QUOTE)

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
