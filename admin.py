from django.contrib import admin

class AbstractAttributeAdmin(admin.ModelAdmin):
    list_display = (
        'key',
        'value',
    )
