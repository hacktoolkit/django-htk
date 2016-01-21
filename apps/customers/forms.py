from django import forms

from htk.apps.customers.utils import get_organization_customer_choices
from htk.forms.classes import AbstractModelInstanceUpdateForm
from htk.forms.utils import set_input_attrs
from htk.forms.utils import set_input_placeholder_labels
from htk.utils import htk_setting
from htk.utils import resolve_model_dynamically

class OrganizationCustomersImportForm(forms.Form):
    organization_customer = forms.ChoiceField(choices=get_organization_customer_choices())
    csv_file = forms.FileField(required=True, label='CSV file', help_text='<b>IMPORTANT:</b> The format of the CSV file* must be exact.')

    def __init__(self, *args, **kwargs):
        super(OrganizationCustomersImportForm, self).__init__(*args, **kwargs)
        self.label_suffix = ''
        set_input_attrs(self)
        set_input_placeholder_labels(self)

    def clean_organization_customer(self):
        organization_customer = None
        organization_customer_id = self.cleaned_data['organization_customer']
        if organization_customer_id:
            OrganizationCustomerModel = resolve_model_dynamically(htk_setting('HTK_CPQ_ORGANIZATION_CUSTOMER_MODEL'))
            try:
                organization_customer = OrganizationCustomerModel.objects.get(id=organization_customer_id)
            except OrganizationCustomerModel.DoesNotExist:
                pass

        if organization_customer is None:
            raise forms.ValidationError('Could not find organization')
        elif organization_customer.members.exists():
            raise forms.ValidationError('Organization already has members. Importing is not allowed, as it would overwrite existing members. To re-import, delete existing members first.')

        self.organization_customer = organization_customer
        return organization_customer

    def clean_csv_file(self):
        csv_file = self.cleaned_data['csv_file']
        self.csv_file = csv_file
        return csv_file

    def save(self, *args, **kwargs):
        customers = None
        if self.organization_customer and self.csv_file:
            from htk.apps.customers.utils import import_organization_customers_from_csv_file
            customers = import_organization_customers_from_csv_file(self.organization_customer, self.csv_file)
        return customers

class CustomerForm(AbstractModelInstanceUpdateForm):
    class Meta:
        model = resolve_model_dynamically(htk_setting('HTK_CPQ_CUSTOMER_MODEL'))
        exclude = ()
