# Customers App

Customer management for commerce and B2B applications.

## Quick Start

```python
from htk.apps.customers.models import BaseCustomer

# Create customer
customer = BaseCustomer.objects.create(
    user=user,
    name='Acme Corp',
    email='procurement@acme.com'
)

# Attach to organization
org_customer = BaseOrganizationCustomer.objects.create(
    organization=org,
    customer=customer,
    role='procurement'
)
```

## Models

- **`BaseCustomer`** - Individual customer
- **`BaseOrganizationCustomer`** - Customer linked to organization

## Common Patterns

```python
# Get all customers for organization
org_customers = org.baseorganizationcustomer_set.all()

# Get customer's purchases/quotes
quotes = customer.cpqquote_set.all()

# Update customer info
customer.name = 'Updated Name'
customer.save()
```

## Integration with CPQ

```python
# Link customer to quotes
quote = BaseCPQQuote.objects.create(customer=customer)
```

## Related Modules

- `htk.apps.cpq` - Quoting system
- `htk.apps.organizations` - Organization management
