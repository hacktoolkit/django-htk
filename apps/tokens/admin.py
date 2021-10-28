# Django Imports
from django.contrib import admin

# HTK Imports
from htk.apps.tokens.utils import get_token_model


Token = get_token_model()


class BaseTokenAdmin(admin.ModelAdmin):
    model = Token

    list_display = (
        'id',
        'key',
        'value',
        'description',
        'is_valid',
        'valid_after',
        'valid_until',
        'created_at',
        'updated_at',
    )

    list_filter = (
        'key',
    )

    search_fields = (
        'key',
        'value',
    )

    def is_valid(self, obj):
        return obj.is_valid


# admin.site.register(Token, BaseTokenAdmin)
