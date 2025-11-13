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

## Usage Examples

### Configure Payment Settings

```python
# In Django settings.py
HTK_CPQ_PAY_ONLINE = True
HTK_CPQ_XOR_KEY = 9876543210987  # Use strong random value
HTK_CPQ_CRYPT_SECRET = 'your-secret-key-here'
```

### Use Custom Templates

```python
# In Django settings.py
HTK_CPQ_TEMPLATE_NAME_INVOICE = 'myapp/cpq/invoice_custom.html'
HTK_CPQ_TEMPLATE_NAME_QUOTE = 'myapp/cpq/quote_custom.html'
```
