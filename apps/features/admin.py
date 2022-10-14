# Django Imports
from django.contrib import admin

# HTK Imports
from htk.apps.features.utils import get_feature_flag_model


FeatureFlagModel = get_feature_flag_model()


class BaseFeatureFlagAdmin(admin.ModelAdmin):
    model = FeatureFlagModel

    list_display = (
        'id',
        'name',
        'description',
        'enabled',
        'enabled_after',
        'disabled_after',
        'created_at',
        'updated_at',
    )


# admin.site.register(FeatureFlagModel, BaseFeatureFlagAdmin)
