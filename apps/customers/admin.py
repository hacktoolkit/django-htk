from django.contrib import admin

from htk.apps.customers.models import CustomerAttribute

class CustomerAttributeInline(admin.TabularInline):
    model = CustomerAttribute
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
