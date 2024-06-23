# Django Imports
from django.contrib import admin
from django.urls import reverse
from django.utils.safestring import mark_safe

# HTK Imports
from htk.apps.prelaunch.loading import PrelaunchSignup
from htk.utils import htk_setting


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
        'created_at',
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
        url_name = htk_setting('HTK_PRELAUNCH_ADMINTOOLS_TOGGLE_URL_NAME')
        url = reverse(url_name, args=(obj.id,))
        value = '<a href="{}" target="_blank">Toggle Early Access</a>'.format(
            url
        )
        return value

    toggle_early_access.allow_tags = True
    toggle_early_access.short_description = 'Toggle Early Access'


admin.site.register(PrelaunchSignup, PrelaunchSignupAdmin)
