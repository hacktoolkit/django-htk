from django.contrib import admin

from htk.apps.feedback.models import Feedback

class FeedbackAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'site',
        'date_created',
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
        'date_created',
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
        ('Date Information', {'fields': ['date_created']}),
        ('Page Viewing', {'fields': ['uri']}),
        ('Submitted Feedback', {'fields': ['name', 'email', 'comment']}),
        ]

    date_hierarchy = 'date_created'

admin.site.register(Feedback, FeedbackAdmin)
