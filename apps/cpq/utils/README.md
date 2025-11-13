# HTK CPQ Utils

Utilities for Quote and Invoice management including URL generation, crypto encoding, and accounting.

## Functions by Category

### Admin/Reporting Functions

**get_admin_urls()**
- Generates Django admin URLs for all CPQ models
- Returns list of dicts with 'url', 'add_url', and 'name' keys
- Uses CPQ_APP_MODEL_NAMES constant for model list

**get_reporting_urls()**
- Generates reporting view URLs for CPQ
- Returns list of dicts with 'url' and 'name' keys
- Uses CPQ_REPORTING_URL_NAMES constant

**get_tools_urls()**
- Generates tools view URLs for CPQ
- Returns list of dicts with 'url' and 'name' keys
- Uses CPQ_TOOLS_URL_NAMES constant

**get_invoice_payment_terms_choices()**
- Gets payment term choices from InvoicePaymentTerm enum
- Returns list of (value, symbolic_name) tuples for form dropdowns

### Crypto Functions

**compute_cpq_code(cpq)**
- Encodes CPQ object ID into checksum-protected code
- Process: XOR with key > add Luhn check digit > base36 encode > prepend MD5 hash
- Returns obfuscated string code for Quote/Invoice display

**compute_cpq_code_check_hash(cpq_code)**
- Generates MD5 hash prefix for CPQ code validation
- Hash length from HTK_CPQ_CHECK_HASH_LENGTH setting
- Used to detect code tampering

**is_valid_cpq_code_check_hash(cpq_code, check_hash)**
- Validates check hash matches code
- Verifies code hasn't been altered
- Returns boolean

**resolve_cpq_code(cpq_code, cpq_type=CPQType.INVOICE)**
- Decodes CPQ code back to object
- Validates check hash and Luhn digit
- Supports INVOICE, QUOTE, and GROUP_QUOTE types
- Returns CPQ object or None if invalid

### Accounting Functions

**get_invoice_years()**
- Gets list of all years with invoices
- Returns list of year integers, ordered chronologically

**get_receivables_by_year(year)**
- Gets paid invoices for specified year
- Filters by invoice_type=INVOICE and paid=True
- Returns QuerySet ordered by date

## Example Usage

```python
from htk.apps.cpq.utils import (
    compute_cpq_code,
    resolve_cpq_code,
    get_invoice_years,
)

# Encode an invoice
invoice = Invoice.objects.get(id=123)
code = compute_cpq_code(invoice)  # Returns: "abc123def456"

# Decode a code
decoded = resolve_cpq_code(code)  # Returns: Invoice object or None

# Get accounting data
years = get_invoice_years()
paid_2024 = get_receivables_by_year(2024)
```
