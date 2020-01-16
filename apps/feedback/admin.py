# Django Imports
from django.contrib import admin

# HTK Imports
from htk.apps.feedback.models import Feedback


class FeedbackAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'site',
        'created_on',
        'user',
        'name',
        'email',
        'comment',
        'uri',
        'processed',
        'needs_followup',
    )

    list_editable = (
        'processed',
        'needs_followup',
    )

    list_filter = (
        'site',
        'created_on',
        'processed',
        'needs_followup',
    )

    search_fields = (
        'name',
        'email',
        'comment',
        'uri',
    )

    readonly_fields = (
        'created_on',
        'site',
        'uri',
        'name',
        'email',
        'comment',
    )

    fieldsets = [
        ('Date Information', {
            'fields': [
                'created_on',
            ],
        }),
        ('Page Viewing', {
            'fields': [
                'site',
                'uri',
            ]
        }),
        ('Submitted Feedback', {
            'fields': [
                'name',
                'email',
                'comment',
            ]
        }),
        ('Admin', {
            'fields' : [
                'processed',
                'needs_followup',
            ]
        }),
    ]

    date_hierarchy = 'created_on'

admin.site.register(Feedback, FeedbackAdmin)
