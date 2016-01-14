from enum import Enum

class CPQType(Enum):
    INVOICE = 1
    QUOTE = 2
    GROUP_QUOTE = 3

class InvoiceType(Enum):
    INVOICE = 1
    REIMBURSEMENT = 10

class InvoicePaymentTerm(Enum):
    PAYMENT_DUE_UPON_RECEIPT = 1
    PAYABLE_NET_14 = 14
    PAYABLE_NET_30 = 30
