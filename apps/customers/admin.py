from django.contrib import admin

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
