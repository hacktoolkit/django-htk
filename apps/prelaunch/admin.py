# Django Imports
from django.contrib import admin
from django.urls import reverse
from django.utils.safestring import mark_safe

# HTK Imports
from htk.apps.prelaunch.loading import PrelaunchSignup


# isort: off


class PrelaunchSignupAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'site',
        'first_name',
        'last_name',
        'email',
        'early_access',
        'early_access_code',
        'toggle_early_access',
        'created_on',
        'updated_at',
    )

    list_filter = ('site',)
    search_fields = (
        'first_name',
        'last_name',
        'email',
    )

    @mark_safe
    def toggle_early_access(self, obj):
        url = reverse('admintools_api_prelaunch_toggle', args=(obj.id,))
        value = '<a href="{}" target="_blank">Toggle Early Access</a>'.format(
            url
        )
        return value

    toggle_early_access.allow_tags = True
    toggle_early_access.short_description = 'Toggle Early Access'


admin.site.register(PrelaunchSignup, PrelaunchSignupAdmin)
