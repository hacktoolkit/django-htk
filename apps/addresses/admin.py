# Django Imports
from django.contrib import admin
from django.utils.safestring import mark_safe


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
        'view_on_map',
    )
    readonly_fields = (
        'latitude',
        'longitude',
        'view_on_map',
    )
    fieldsets = (
        (None,
         {
             'fields' : (
                 'name',
                 'latitude',
                 'longitude',
                 'view_on_map',
             ),
         }
        ),
        ('Address',
         {
             'fields' : (
                 'street',
                 'city',
                 'state',
                 'zipcode',
                 'country',
             ),
         }
        ),
        ('Address Parts',
         {
             'fields' : (
                 'street_number',
                 'street_name',
                 'unit_type',
                 'unit',
             ),
         }
        )
    )

    @mark_safe
    def view_on_map(self, obj):
        value = '<a href="%s" target=_blank">View on Map</a>' % obj.map_url()
        return value
    view_on_map.allow_tags = True
    view_on_map.short_description = 'View on Map'
