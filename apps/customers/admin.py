from django.contrib import admin

from htk.apps.customers.models import CustomerAttribute
from htk.apps.customers.models import OrganizationCustomerAttribute

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
        'name',
        'attention',
        'email',
        'address',
        'mailing_address',
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
