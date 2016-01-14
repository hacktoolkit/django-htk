from htk.utils.enums import get_enum_symbolic_name
from htk.utils import htk_setting
from htk.utils import resolve_model_dynamically

def get_organization_type_choices():
    from htk.apps.customers.enums import OrganizationType
    choices = [(organization_type.value, get_enum_symbolic_name(organization_type),) for organization_type in OrganizationType]
    return choices

def get_organization_customer_choices():
    OrganizationCustomerModel = resolve_model_dynamically(htk_setting('HTK_CPQ_ORGANIZATION_CUSTOMER_MODEL'))
    choices = [('', 'Select an Organization Customer',)]
    choices += [(org.id, org,) for org in OrganizationCustomerModel.objects.all()]
    return choices

def import_organization_customers_from_csv_file(organization_customer, csv_file):
    import csv
    allowed_columns = (
        'last_name, first_name',
        'first_name',
        'last_name',
        'email',
        'address',
        'address_city',
        'address_state',
        'address_zipcode',
        'mailing_address',
        'mailing_address2',
        'mailing_city',
        'mailing_state',
        'mailing_zipcode',
    )
    allowed_columns_dict = { k : True for k in allowed_columns }
    column_mapping = {}
    customers = []
    # https://docs.python.org/2/library/csv.html#csv.DictReader
    # csv.DictReader reads the first row as fieldnames
    reader = csv.DictReader(csv_file.file.read().splitlines())
    for row in reader:
        customer_data = { k : v.strip() for k, v in row.iteritems() }
        if 'last_name, first_name' in customer_data:
            (last_name, first_name,) = [name.strip() for name in customer_data['last_name, first_name'].split(',', 1)]
            customer_data['first_name'] = first_name
            customer_data['last_name'] = last_name
        first_name = customer_data.get('first_name', '')
        last_name = customer_data.get('last_name', '')
        name = '%s%s%s' % (first_name, ' ' if first_name else '', last_name,)
        customer_data['name'] = name
        if 'mailing_address' in customer_data and 'mailing_address2' in customer_data:
            mailing_address2 = customer_data.pop('mailing_address2', '')
            if mailing_address2:
                customer_data['mailing_address'] += ', %s' % mailing_address2
        customer = create_organization_customer_member(organization_customer, customer_data)
        customers.append(customer)
    return customers

def create_organization_customer_member(organization_customer, customer_data):
    from htk.apps.addresses.forms import PostalAddressForm
    from htk.apps.customers.forms import CustomerForm
    address_data = {
        'name' : customer_data.get('name', ''),
        'street' : customer_data.pop('address', ''),
        'city' : customer_data.pop('address_city', ''),
        'state' : customer_data.pop('address_state', ''),
        'zipcode' : customer_data.pop('address_zipcode', ''),
    }
    mailing_address_data = {
        'name' : customer_data.get('name', ''),
        'street' : customer_data.pop('mailing_address', ''),
        'city' : customer_data.pop('mailing_city', ''),
        'state' : customer_data.pop('mailing_state', ''),
        'zipcode' : customer_data.pop('mailing_zipcode', ''),
    }

    customer = None
    address = None
    mailing_address = None
    address_form = PostalAddressForm(None, address_data)
    if address_form.is_valid():
        address = address_form.save()
        customer_data['address'] = address.id
    if address_data != mailing_address_data:
        mailing_address_form = PostalAddressForm(None, mailing_address_data)
        if mailing_address_form.is_valid():
            mailing_address = mailing_address_form.save()
            customer_data['mailing_address'] = mailing_address.id
    customer_data['organization'] = organization_customer.id
    customer_form = CustomerForm(None, customer_data)
    if customer_form.is_valid():
        customer = customer_form.save()
    else:
        customer = None
    return customer
