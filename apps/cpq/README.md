# CPQ App (Configure, Price, Quote)

Quoting and invoicing system for B2B commerce.

## Overview

The `cpq` app provides:

- Create quotes for customers
- Line items with pricing and customization
- Convert quotes to invoices
- Payment processing with Stripe
- Quote history and tracking
- Group quotes for bulk orders

## Quick Start

### Create Quotes

```python
from htk.apps.cpq.models import BaseCPQQuote, BaseCPQQuoteLineItem

# Create quote
quote = BaseCPQQuote.objects.create(
    customer_name='Acme Corp',
    customer_email='procurement@acme.com',
    expires_at=timezone.now() + timedelta(days=30)
)

# Add line items
line_item = BaseCPQQuoteLineItem.objects.create(
    quote=quote,
    description='Enterprise License',
    quantity=1,
    unit_price=1000.00
)

quote.refresh_from_db()  # Updates total
```

### Approve & Payment

```python
# Approve and process payment
quote.approve_and_pay(
    line_item_ids=[line_item.id],
    amount=1000.00,
    stripe_token='tok_xxx'
)

# Creates invoice automatically
```

### Group Quotes

```python
from htk.apps.cpq.models import BaseCPQGroupQuote

# Create group quote (for parent-child relationships)
group_quote = BaseCPQGroupQuote.objects.create(
    name='Q4 Regional Sales'
)

# Add sub-quotes
quote1.group_quote = group_quote
quote1.save()

# Sync amounts
group_quote.sync_group_sub_quotes()
```

## Models

- **`BaseCPQQuote`** - Main quote model
- **`BaseCPQGroupQuote`** - Group multiple quotes
- **`BaseCPQInvoice`** - Invoice from approved quote
- **`BaseCPQQuoteLineItem`** - Line items in quote
- **`BaseCPQInvoiceLineItem`** - Line items in invoice

## Workflow

```
Create Quote
    ↓
Add Line Items
    ↓
Send to Customer
    ↓
Customer Approves
    ↓
Process Payment (Stripe)
    ↓
Create Invoice
    ↓
Customer Pays
```

## Common Patterns

### Sending Quotes

```python
from htk.apps.cpq.emailers import send_quote_email

# Send quote to customer
send_quote_email(
    quote=quote,
    recipient_email='buyer@acme.com'
)
```

### Payment Recording

```python
# Record Stripe payment
quote.record_payment(
    charge_id='ch_xxx',
    amount=1000.00,
    line_items=[line_item]
)

# Creates invoice
invoice = quote.create_invoice_for_payment(
    stripe_customer=customer,
    line_items=[line_item]
)
```

### Quote Encoding

```python
from htk.apps.cpq.utils.crypto import compute_cpq_code, resolve_cpq_code

# Encode quote/invoice for URL
code = compute_cpq_code(quote)

# Decode from URL
obj = resolve_cpq_code(code)  # Returns Quote or Invoice
```

## Dashboard & Reporting

```python
# Built-in URL patterns
# cpq_dashboard - Overview of all quotes
# cpq_invoices_index - List of invoices
# cpq_quotes_index - List of quotes
# cpq_receivables - Payment tracking by year
```

## Configuration

```python
# settings.py
CPQ_QUOTE_EXPIRY_DAYS = 30
CPQ_REQUIRE_APPROVAL = True
CPQ_STRIPE_CONNECTED = True
```

## Best Practices

1. **Set expiration dates** on all quotes
2. **Use line item descriptions** clearly
3. **Record all payments** for audit trail
4. **Send email confirmations** when quote created
5. **Track quote status** for follow-ups
6. **Use group quotes** for related deals
