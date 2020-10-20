# Django Imports
from django.contrib import admin

# HTK Imports
from htk.utils import htk_setting
from htk.utils.general import resolve_model_dynamically


FeatureFlagModel = resolve_model_dynamically(htk_setting('HTK_FEATURE_FLAG_MODEL'))


class BaseFeatureFlagAdmin(admin.ModelAdmin):
    model = FeatureFlagModel

    list_display = (
        'id',
        'name',
        'enabled',
        'enabled_after',
        'disabled_after',
        'created_at',
        'updated_at',
    )


# admin.site.register(FeatureFlagModel, BaseFeatureFlagAdmin)
