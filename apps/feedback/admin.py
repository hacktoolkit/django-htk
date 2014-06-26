from django.contrib import admin

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

    fieldsets = [
        ('Date Information', {'fields': ['created_on']}),
        ('Page Viewing', {'fields': ['uri']}),
        ('Submitted Feedback', {'fields': ['name', 'email', 'comment']}),
        ]

    date_hierarchy = 'created_on'

admin.site.register(Feedback, FeedbackAdmin)
