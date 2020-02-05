# Python Standard Library Imports
import hashlib

# Django Imports
from django.conf import settings
from django.utils.http import base36_to_int
from django.utils.http import int_to_base36

# HTK Imports
from htk.apps.cpq.enums import CPQType
from htk.utils import htk_setting
from htk.utils.general import resolve_model_dynamically
from htk.utils.luhn import calculate_luhn
from htk.utils.luhn import is_luhn_valid


CPQ_XOR_KEY = htk_setting('HTK_CPQ_XOR_KEY')
CPQ_CHECK_HASH_LENGTH = htk_setting('HTK_CPQ_CHECK_HASH_LENGTH')

def compute_cpq_code(cpq):
    """Computes the encoded id for a CPQ object (Quote or Invoice)
    """
    xored = cpq.id ^ CPQ_XOR_KEY
    check_digit = calculate_luhn(xored)
    padded = int(str(xored) + str(check_digit))
    cpq_code = int_to_base36(padded)
    check_hash = compute_cpq_code_check_hash(cpq_code)
    cpq_code = check_hash + cpq_code
    return cpq_code

def compute_cpq_code_check_hash(cpq_code):
    check_hash = hashlib.md5(cpq_code.encode()).hexdigest()[:CPQ_CHECK_HASH_LENGTH]
    return check_hash

def is_valid_cpq_code_check_hash(cpq_code, check_hash):
    verify_hash = compute_cpq_code_check_hash(cpq_code)
    is_valid = verify_hash == check_hash
    return is_valid

def resolve_cpq_code(cpq_code, cpq_type=CPQType.INVOICE):
    """Returns the CPQ object (Quote or Invoice) for this `cpq_code`
    """
    check_hash = cpq_code[:CPQ_CHECK_HASH_LENGTH]
    cpq_code = cpq_code[CPQ_CHECK_HASH_LENGTH:]
    if is_valid_cpq_code_check_hash(cpq_code, check_hash):
        if cpq_type == CPQType.INVOICE:
            CPQModel = resolve_model_dynamically(settings.HTK_CPQ_INVOICE_MODEL)
        elif cpq_type == CPQType.QUOTE:
            CPQModel = resolve_model_dynamically(settings.HTK_CPQ_QUOTE_MODEL)
        elif cpq_type == CPQType.GROUP_QUOTE:
            CPQModel = resolve_model_dynamically(settings.HTK_CPQ_GROUP_QUOTE_MODEL)
        else:
            raise Exception('Bad value for cpq_type')
        try:
            padded = base36_to_int(cpq_code)
            if is_luhn_valid(padded):
                xored = padded // 10
                cpq_id = xored ^ CPQ_XOR_KEY
                cpq = CPQModel.objects.get(id=cpq_id)
            else:
                cpq = None
        except ValueError:
            cpq = None
        except CPQModel.DoesNotExist:
            cpq = None
    else:
        cpq = None
    return cpq
