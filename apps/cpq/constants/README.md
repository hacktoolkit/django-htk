# CPQ (Configure, Price, Quote) Constants

## Overview

This module defines configuration for the CPQ system, including payment settings, encryption keys, and template paths for quotes and invoices.

## Constants

### Payment Configuration

- **`HTK_CPQ_PAY_ONLINE`** - Default: `False` - Enable online payment processing
- **`HTK_CPQ_XOR_KEY`** - Default: `1234567890123` - XOR encryption key for quote IDs
- **`HTK_CPQ_CRYPT_SECRET`** - Default: `'Zu7ooqu8'` - Encryption secret for sensitive data
- **`HTK_CPQ_CHECK_HASH_LENGTH`** - Default: `5` - Length of hash for validation checks

### Template Configuration

- **`HTK_CPQ_TEMPLATE_NAME_DASHBOARD`** - Default: `'htk/fragments/cpq/invoice.html'`
- **`HTK_CPQ_TEMPLATE_NAME_INVOICE`** - Default: `'htk/fragments/cpq/invoice.html'`
- **`HTK_CPQ_TEMPLATE_NAME_QUOTE`** - Default: `'htk/fragments/cpq/quote.html'`
- **`HTK_CPQ_TEMPLATE_NAME_GROUP_QUOTE`** - Default: `'htk/fragments/cpq/group_quote.html'`
- **`HTK_CPQ_TEMPLATE_NAME_GROUP_QUOTE_ALL`** - Default: `'htk/fragments/cpq/group_quote_all.html'`
- **`HTK_CPQ_TEMPLATE_NAME_RECEIVABLES`** - Default: `'htk/fragments/cpq/receivables.html'`
- **`HTK_CPQ_TEMPLATE_NAME_IMPORT_CUSTOMERS`** - Default: `'htk/fragments/cpq/import_customers.html'`

### URL Configuration

- **`CPQ_APP_MODEL_NAMES`** - List of models in CPQ app for admin urls
- **`CPQ_REPORTING_URL_NAMES`** - List of reporting view URL names
- **`CPQ_TOOLS_URL_NAMES`** - List of tools/utility view URL names

## Enums

### CPQType

Document types in the CPQ system:

```python
from htk.apps.cpq.enums import CPQType

# Available CPQ types with values
CPQType.INVOICE          # value: 1
CPQType.QUOTE            # value: 2
CPQType.GROUP_QUOTE      # value: 3

# Access enum properties
doc_type = CPQType.INVOICE
print(f"{doc_type.name}: {doc_type.value}")  # INVOICE: 1
```

### InvoiceType

Invoice categorization:

```python
from htk.apps.cpq.enums import InvoiceType

InvoiceType.INVOICE          # value: 1
InvoiceType.REIMBURSEMENT    # value: 10
```

### InvoicePaymentTerm

Payment terms for invoices:

```python
from htk.apps.cpq.enums import InvoicePaymentTerm

InvoicePaymentTerm.PAYMENT_DUE_UPON_RECEIPT    # value: 1
InvoicePaymentTerm.PAYABLE_NET_14              # value: 14
InvoicePaymentTerm.PAYABLE_NET_30              # value: 30
```

## Usage Examples

### Configure Payment Settings

```python
# In Django settings.py
HTK_CPQ_PAY_ONLINE = True
HTK_CPQ_XOR_KEY = 9876543210987  # Use strong random value
HTK_CPQ_CRYPT_SECRET = 'your-secret-key-here'
```

### Create Quote with CPQType

```python
from htk.apps.cpq.enums import CPQType

quote_type = CPQType.QUOTE.value
# Store in database as integer value
```

### Set Payment Terms

```python
from htk.apps.cpq.enums import InvoicePaymentTerm

invoice.payment_term = InvoicePaymentTerm.PAYABLE_NET_30.value
invoice.save()
```

### Use Custom Templates

```python
# In Django settings.py
HTK_CPQ_TEMPLATE_NAME_INVOICE = 'myapp/cpq/invoice_custom.html'
HTK_CPQ_TEMPLATE_NAME_QUOTE = 'myapp/cpq/quote_custom.html'
```
