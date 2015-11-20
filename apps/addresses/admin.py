from django.contrib import admin

class BasePostalAddressAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'name',
        'street',
        'city',
        'state',
        'zipcode',
        'country',
        # computed parts
        'street_number',
        'street_name',
        'unit_type',
        'unit',
        'latitude',
        'longitude',
    )
