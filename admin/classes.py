# Python Standard Library Imports

# Third Party / PIP Imports

# Django Imports
from django.contrib import admin


class AbstractAttributeAdmin(admin.ModelAdmin):
    list_display = (
        'key',
        'value',
    )
