import hashlib

from django.conf import settings
from django.utils.http import base36_to_int
from django.utils.http import int_to_base36

from htk.utils import htk_setting
from htk.utils.general import resolve_model_dynamically
from htk.utils.luhn import calculate_luhn
from htk.utils.luhn import is_luhn_valid

INVOICE_XOR_KEY = htk_setting('HTK_INVOICE_XOR_KEY')
INVOICE_CHECK_HASH_LENGTH = htk_setting('HTK_INVOICE_CHECK_HASH_LENGTH')

def compute_invoice_code(invoice):
    """Computes the encoded id for an Invoice
    """
    xored = invoice.id ^ INVOICE_XOR_KEY
    check_digit = calculate_luhn(xored)
    padded = int(str(xored) + str(check_digit))
    invoice_code = int_to_base36(padded)
    check_hash = compute_invoice_code_check_hash(invoice_code)
    invoice_code = check_hash + invoice_code
    return invoice_code

def compute_invoice_code_check_hash(invoice_code):
    check_hash = hashlib.md5(invoice_code).hexdigest()[:INVOICE_CHECK_HASH_LENGTH]
    return check_hash

def is_valid_invoice_code_check_hash(invoice_code, check_hash):
    verify_hash = compute_invoice_code_check_hash(invoice_code)
    is_valid = verify_hash == check_hash
    return is_valid

def resolve_invoice_code(invoice_code):
    """Returns the Invoice for this `invoice_code`
    """
    check_hash = invoice_code[:INVOICE_CHECK_HASH_LENGTH]
    invoice_code = invoice_code[INVOICE_CHECK_HASH_LENGTH:]
    if is_valid_invoice_code_check_hash(invoice_code, check_hash):
        InvoiceModel = resolve_model_dynamically(settings.HTK_INVOICE_MODEL)
        try:
            padded = base36_to_int(invoice_code)
            if is_luhn_valid(padded):
                xored = padded / 10
                invoice_id = xored ^ INVOICE_XOR_KEY
                invoice = InvoiceModel.objects.get(id=invoice_id)
            else:
                invoice = None
        except ValueError:
            invoice = None
        except InvoiceModel.DoesNotExist:
            invoice = None
    else:
        invoice = None
    return invoice
