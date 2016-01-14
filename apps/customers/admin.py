from django.contrib import admin

from htk.apps.customers.models import CustomerAttribute
from htk.apps.customers.models import OrganizationCustomerAttribute
from htk.utils import htk_setting
from htk.utils import resolve_model_dynamically

class CustomerAttributeInline(admin.TabularInline):
    model = CustomerAttribute
    extra = 0
    can_delete = True

class OrganizationCustomerAttributeInline(admin.TabularInline):
    model = OrganizationCustomerAttribute
    extra = 0
    can_delete = True

class BaseCustomerAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'user',
        'organization',
        'name',
        'attention',
        'email',
        'address',
        'mailing_address',
    )
    list_filter = (
        'organization',
    )
    inlines = (
        CustomerAttributeInline,
    )

class BaseOrganizationCustomerAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'name',
        'attention',
        'email',
        'address',
        'mailing_address',
    )
    inlines = (
        OrganizationCustomerAttributeInline,
    )
