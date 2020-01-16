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
