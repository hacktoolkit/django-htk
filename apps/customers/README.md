# Customers App

Customer management for commerce and B2B applications.

## Quick Start

```python
from htk.apps.customers.models import BaseCustomer, BaseOrganizationCustomer

# Create customer
customer = BaseCustomer.objects.create(
    user=user,
    name='Acme Corp',
    email='procurement@acme.com'
)

# Link customer to organization
org_customer = BaseOrganizationCustomer.objects.create(
    organization=org,
    customer=customer,
    role='procurement_manager'
)

# Get customer's quotes
quotes = customer.cpqquote_set.all()
```

## Customer Models

### BaseCustomer

Individual customer entity (can be internal or external):

```python
from htk.apps.customers.models import BaseCustomer

# Create customer with user
customer = BaseCustomer.objects.create(
    user=user,
    name='John Doe',
    email='john@example.com'
)

# Or without user (for external customers)
external = BaseCustomer.objects.create(
    name='External Partner',
    email='partner@external.com'
)

# Query customers
my_customers = BaseCustomer.objects.filter(user=request.user)
```

### BaseOrganizationCustomer

Customer linked to an organization with roles:

```python
from htk.apps.customers.models import BaseOrganizationCustomer

# Create org customer
org_customer = BaseOrganizationCustomer.objects.create(
    organization=org,
    customer=customer,
    role='procurement_manager'
)

# Get all customers for org
org_customers = org.baseorganizationcustomer_set.all()

# Filter by role
managers = org.baseorganizationcustomer_set.filter(role='procurement_manager')
```

## Common Patterns

### Customer Hierarchy

```python
from htk.apps.customers.models import BaseCustomer, BaseOrganizationCustomer

# Create customer linked to multiple orgs
customer = BaseCustomer.objects.create(user=user, name='Acme')

# Add to multiple organizations
for org in organizations:
    BaseOrganizationCustomer.objects.create(
        organization=org,
        customer=customer,
        role='buyer'
    )

# Get all orgs for customer
orgs = [oc.organization for oc in customer.baseorganizationcustomer_set.all()]
```

### Customer Searches and Filtering

```python
from django.db.models import Q
from htk.apps.customers.models import BaseCustomer

# Search by name or email
customers = BaseCustomer.objects.filter(
    Q(name__icontains='acme') | Q(email__icontains='acme')
)

# Get customers with quotes
customers_with_quotes = BaseCustomer.objects.filter(
    cpqquote__isnull=False
).distinct()

# Get organization customers
from htk.apps.customers.models import BaseOrganizationCustomer
org_customers = BaseOrganizationCustomer.objects.filter(
    organization=org,
    role__in=['buyer', 'approver']
)
```

### Customer Activity Tracking

```python
from django.utils import timezone
from htk.apps.customers.models import BaseOrganizationCustomer

# Track last quote/order date
customer = BaseOrganizationCustomer.objects.get(id=customer_id)
latest_quote = customer.customer.cpqquote_set.order_by('-created').first()

# Identify inactive customers (no activity in 90 days)
from datetime import timedelta
cutoff = timezone.now() - timedelta(days=90)
inactive = BaseCustomer.objects.filter(
    cpqquote__created__lt=cutoff
).distinct()
```

## Integration with CPQ

Link customers to quotes and orders:

```python
from htk.apps.cpq.models import BaseCPQQuote

# Create quote for customer
quote = BaseCPQQuote.objects.create(
    customer=customer,
    name='Q2024-001',
    amount=10000.00
)

# Get customer's quotes
quotes = customer.cpqquote_set.filter(status='sent')
total_value = sum(q.amount for q in quotes)
```

## Configuration

```python
# settings.py
CUSTOMER_MODELS = {
    'base': 'myapp.models.CustomCustomer',
}

# Custom roles for organization customers
CUSTOMER_ROLES = [
    ('buyer', 'Buyer'),
    ('approver', 'Approver'),
    ('procurement_manager', 'Procurement Manager'),
]
```

## Best Practices

1. **Organize by roles** - Use role field for permission-based filtering
2. **Link to organizations** - Use BaseOrganizationCustomer for multi-org support
3. **Track customer hierarchy** - Maintain parent-child relationships
4. **Index by email** - Add database index on email for fast lookups
5. **Audit customer changes** - Track modifications for compliance
