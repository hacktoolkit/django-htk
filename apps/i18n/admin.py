# Django Imports
from django.contrib import admin

# HTK Imports
from htk.utils import (
    htk_setting,
    resolve_model_dynamically,
)


class LocalizedStringInline(admin.TabularInline):
    model = resolve_model_dynamically(htk_setting('HTK_LOCALIZED_STRING_MODEL'))
    extra = 0
    can_delete = True


class AbstractLocalizableStringAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'key',
        'context',
        'description',
        'default_translation',
        'available_translations',
    )

    inlines = (LocalizedStringInline,)

    def default_translation(self, obj):
        translation = obj.translations.filter(language_code='en-US').first()
        value = translation.value if translation else None
        return value

    def available_translations(self, obj):
        translations = list(
            obj.translations.values_list('language_code', flat=True)
        )
        return translations


class AbstractLocalizedStringAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'localizable_string',
        'language_code',
        'value',
    )
