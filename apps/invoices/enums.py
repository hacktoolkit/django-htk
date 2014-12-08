from enum import Enum

class InvoiceType(Enum):
    INVOICE = 1
    REIMBURSEMENT = 10

class InvoicePaymentTerm(Enum):
    PAYMENT_DUE_UPON_RECEIPT = 1
    PAYABLE_NET_30 = 30
