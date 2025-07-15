# Django Imports
from django.contrib import admin


class BaseReleaseAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'name',
        'repository',
        'tag_name',
        'draft',
        'prerelease',
        'released_at',
        'published_at',
        'created_at',
        'updated_at',
    )

    list_editable = ('released_at',)
