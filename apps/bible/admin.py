# Python Standard Library Imports

# Third Party / PIP Imports

# Django Imports
from django.contrib import admin
from django.db import models

# HTK Imports


class AbstractBibleBookAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'name',
        'testament',
    )


class AbstractBibleChapterAdmin(admin.ModelAdmin):
    list_display = (
        'id',
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
