# Cpq

## Classes
- **`AbstractCPQQuote`** (cpq/models.py) - Abstract base class for a Quote, Invoice, or GroupQuote
- **`BaseCPQQuote`** (cpq/models.py) - Base class for a Quote
- **`BaseCPQGroupQuote`** (cpq/models.py) - Base class for a GroupQuote
- **`BaseCPQInvoice`** (cpq/models.py) - Base class for an Invoice

## Functions
- **`sync_group_sub_quotes`** (cpq/apps.py) - signal handler for GroupQuote post-save
- **`get_url_name`** (cpq/models.py) - Gets the url_name for this object
- **`resolve_line_item_ids`** (cpq/models.py) - Resolves `line_item_ids` into their respective GroupQuoteLineItems or QuoteLineItems
- **`approve_and_pay`** (cpq/models.py) - Approve `line_item_ids` and pay `amount` for them with a verified `stripe_token`
- **`create_invoice_for_payment`** (cpq/models.py) - Creates an invoice for this Quote with successful payment by `stripe_customer` for `line_items`
- **`record_payment`** (cpq/models.py) - Record an actual Stripe payment for `line_items`
- **`get_charges`** (cpq/models.py) - Get charges made on this Invoice
- **`compute_cpq_code`** (cpq/utils/crypto.py) - Computes the encoded id for a CPQ object (Quote or Invoice)
- **`resolve_cpq_code`** (cpq/utils/crypto.py) - Returns the CPQ object (Quote or Invoice) for this `cpq_code`
- **`cpq_view`** (cpq/views.py) - Renders an invoice, quote, or group quote

## Components
**Models** (`models.py`), **Views** (`views.py`)

## URL Patterns
- `cpq_invoices_index`
- `cpq_invoices_invoice`
- `cpq_groupquotes_index`
- `cpq_groupquotes_quote`
- `cpq_groupquotes_quote_all`
- `cpq_quotes_index`
- `cpq_quotes_quote`
- `cpq_quotes_quote_pay`
- `cpq_index`
- `cpq_dashboard`
- `cpq_receivables`
- `cpq_receivables_by_year`
- `cpq_import_customers`
