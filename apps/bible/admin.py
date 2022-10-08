# Python Standard Library Imports

# Django Imports
from django.contrib import admin
from django.db import models


class AbstractBibleBookAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'name',
        'testament',
    )
    readonly_fields = (
        'name',
        'testament',
    )


class AbstractBibleChapterAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'book',
        'chapter',
    )
    readonly_fields = (
        'book',
        'chapter',
    )


class AbstractBibleVerseAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'book',
        'chapter',
        'verse',
    )
    readonly_fields = (
        'book',
        'chapter',
        'verse',
    )


class AbstractBiblePassageAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'book',
        'chapter_start',
        'verse_start',
        'chapter_end',
        'verse_end',
    )

    readonly_fields = (
        'book',
        'chapter_start',
        'verse_start',
        'chapter_end',
        'verse_end',
    )

    # NOTE:
    # While it can be a noble and valiant attempt to be able to edit fields for Bible passages, this can easily result in errors in data entry.
    # The commented out code that follows is an example of how one might go about doing so.

    # def get_readonly_fields(self, request, obj=None):
    #     """Make editable while creating, but readonly while editing.

    #     See:
    #     - https://stackoverflow.com/a/4346448/865091
    #     - https://code.djangoproject.com/ticket/15602
    #     """
    #     if obj:
    #         # editing an existing object
    #         readonly_fields = self.readonly_fields + (
    #             'book',
    #             'chapter_start',
    #             'verse_start',
    #             'chapter_end',
    #             'verse_end',
    #         )
    #     else:
    #         readonly_fields = self.readonly_fields

    #     return readonly_fields
