from django.conf import settings

from htk.apps.cpq.enums import CPQType
from htk.utils import htk_setting
from htk.utils.general import resolve_model_dynamically

def get_invoice_years():
    InvoiceModel = resolve_model_dynamically(settings.HTK_CPQ_INVOICE_MODEL)
    invoice_years = [d.year for d in InvoiceModel.objects.dates('date', 'year')]
    return invoice_years

def get_receivables_by_year(year):
    InvoiceModel = resolve_model_dynamically(settings.HTK_CPQ_INVOICE_MODEL)
    receivables = InvoiceModel.objects.filter(
        invoice_type=CPQType.INVOICE.value,
        date__year=year,
        paid=True
    ).order_by(
        'date'
    )
    return receivables
