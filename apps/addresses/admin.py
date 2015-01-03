from django.contrib import admin

class BasePostalAddressAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'name',
        'street_number',
        'street',
        'unit',
        #'unit_type',
        'city',
        'state',
        'zipcode',
        'country',
    )
