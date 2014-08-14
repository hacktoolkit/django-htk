from django.contrib import admin

class BasePostalAddressAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'street',
        'unit',
        #'unit_type',
        'city',
        'state',
        'zipcode',
        'country',
    )
