# Django Imports
from django.contrib import admin

# HTK Imports
from htk.apps.feedback.models import Feedback
from htk.apps.feedback.models import FeedbackRequest
from htk.apps.feedback.models import FeedbackRequestComment
from htk.apps.feedback.models import FeedbackRequestVote
from htk.utils import htk_setting


class FeedbackAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'site',
        'created_on',
        'user',
        'comment',
        'uri',
        'needs_followup',
    )

    list_editable = (
        'needs_followup',
    )

    list_filter = (
        'site',
        'created_on',
        'needs_followup',
    )

    search_fields = (
        'comment',
        'uri',
    )

    readonly_fields = (
        'created_on',
        'site',
        'uri',
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
                        'needs_followup',
            ]
        }),
    ]

    date_hierarchy = 'created_on'


class FeedbackRequestCommentInline(admin.TabularInline):
    model = FeedbackRequestComment
    extra = 0
    readonly_fields = (
        'created_on',
        'updated_on',
    )


class FeedbackRequestAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'title',
        'created_by',
        'created_on',
        'site',
        'request_type',
        'status',
        'visibility',
        'owner',
        'votes_count',
        'upvotes_count',
        'downvotes_count',
        'comments_count',
        'needs_review',
        'is_hidden',
        'is_spam',
    )
    list_editable = (
        'status',
        'visibility',
        'owner',
        'needs_review',
        'is_hidden',
        'is_spam',
    )
    list_filter = (
        'site',
        'request_type',
        'status',
        'visibility',
        'created_by',
        'owner',
        'needs_review',
        'is_hidden',
        'is_spam',
        'created_on',
    )
    search_fields = (
        'title',
        'description',
        'created_by__email',
        'source_uri',
    )
    raw_id_fields = (
        'created_by',
        'owner',
    )
    readonly_fields = (
        'votes_count',
        'upvotes_count',
        'downvotes_count',
        'comments_count',
        'created_on',
        'updated_on',
    )
    date_hierarchy = 'created_on'
    inlines = [
        FeedbackRequestCommentInline,
    ]

    actions = (
        'mark_needs_review',
        'hide_requests',
    )

    def mark_needs_review(self, request, queryset):
        queryset.update(needs_review=True)

    def hide_requests(self, request, queryset):
        queryset.update(is_hidden=True)


class FeedbackRequestVoteAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'feedback',
        'user',
        'value',
        'is_active',
        'is_spam',
        'created_on',
    )
    list_filter = (
        'is_active',
        'is_spam',
        'value',
        'created_on',
    )
    search_fields = (
        'feedback__title',
    )


class FeedbackRequestCommentAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'feedback',
        'user',
        'is_internal',
        'is_hidden',
        'is_spam',
        'created_on',
    )
    list_filter = (
        'is_internal',
        'is_hidden',
        'is_spam',
        'created_on',
    )
    search_fields = (
        'feedback__title',
        'comment',
    )


if htk_setting('HTK_FEEDBACK_ENABLE_LEGACY_ADMIN', True):
    admin.site.register(Feedback, FeedbackAdmin)

admin.site.register(FeedbackRequest, FeedbackRequestAdmin)
admin.site.register(FeedbackRequestVote, FeedbackRequestVoteAdmin)
admin.site.register(FeedbackRequestComment, FeedbackRequestCommentAdmin)
