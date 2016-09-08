from django.contrib import admin

class BaseUSZipCodeAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'zip_code',
        'state',
        'city',
        # computed parts
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
                 'latitude',
                 'longitude',
                 'view_on_map',
             ),
         }
        ),
    )

    def view_on_map(self, obj):
        value = u'<a href="%s" target=_blank">View on Map</a>' % obj.map_url()
        return value
    view_on_map.allow_tags = True
    view_on_map.short_description = 'View on Map'
