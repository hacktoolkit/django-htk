# Django Imports
from django.contrib import admin

# HTK Imports
from htk.apps.prelaunch.models import PrelaunchSignup


class PrelaunchSignupAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'site',
        'full_name',
        'email',
        'created_on',
    )

    list_filter = (
        'site',
    )


admin.site.register(PrelaunchSignup, PrelaunchSignupAdmin)
