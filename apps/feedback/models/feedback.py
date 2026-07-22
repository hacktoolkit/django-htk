# Django Imports
from django.conf import settings
from django.contrib.sites.models import Site
from django.db import models

# HTK Imports
from htk.apps.feedback.constants import *
from htk.models import HtkBaseModel


class FeedbackRequest(HtkBaseModel):
    """A public/semi-public idea, feature request, bug, or feedback item."""

    site = models.ForeignKey(Site, related_name='feedback_requests', on_delete=models.CASCADE)
    request_type = models.CharField(max_length=32, choices=FEEDBACK_REQUEST_TYPE_CHOICES, default=FEEDBACK_REQUEST_TYPE_FEATURE)
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    status = models.CharField(max_length=32, choices=FEEDBACK_STATUS_CHOICES, default=FEEDBACK_STATUS_NEW)
    visibility = models.CharField(max_length=24, choices=FEEDBACK_VISIBILITY_CHOICES, default=FEEDBACK_VISIBILITY_PRIVATE)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='created_feedback_requests', null=True, blank=True, default=None, on_delete=models.SET_DEFAULT)
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='owned_feedback_requests', null=True, blank=True, default=None, on_delete=models.SET_DEFAULT)
    source_uri = models.CharField(max_length=1024, blank=True)
    user_agent = models.CharField(max_length=512, blank=True)
    referrer = models.CharField(max_length=1024, blank=True)
    context = models.JSONField(default=dict, blank=True)
    metadata = models.JSONField(default=dict, blank=True)
    votes_count = models.IntegerField(default=0)
    upvotes_count = models.PositiveIntegerField(default=0)
    downvotes_count = models.PositiveIntegerField(default=0)
    comments_count = models.PositiveIntegerField(default=0)
    is_hidden = models.BooleanField(default=False)
    is_spam = models.BooleanField(default=False)
    needs_review = models.BooleanField(default=True)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ('-votes_count', '-created_on')
        indexes = (
            models.Index(fields=('site', 'status')),
            models.Index(fields=('site', 'request_type')),
            models.Index(fields=('site', 'visibility')),
            models.Index(fields=('site', 'created_on')),
        )
        verbose_name = 'Feedback request'
        verbose_name_plural = 'Feedback requests'

    def __str__(self):
        return self.title

    @property
    def is_public(self):
        return self.visibility == FEEDBACK_VISIBILITY_PUBLIC and not self.is_hidden and not self.is_spam

    @property
    def is_open_for_voting(self):
        return self.status not in (FEEDBACK_STATUS_SHIPPED, FEEDBACK_STATUS_DECLINED, FEEDBACK_STATUS_MERGED)

    @property
    def display_name(self):
        if self.created_by_id:
            full_name = self.created_by.get_full_name()
            return full_name or self.created_by.get_username()
        return ''

    def refresh_counts(self, save=True):
        active_votes = self.votes.filter(is_active=True, is_spam=False)
        self.upvotes_count = active_votes.filter(value=FEEDBACK_VOTE_UP).count()
        self.downvotes_count = active_votes.filter(value=FEEDBACK_VOTE_DOWN).count()
        self.votes_count = self.upvotes_count - self.downvotes_count
        self.comments_count = self.comments.filter(is_hidden=False, is_spam=False).count()
        if save:
            self.save(update_fields=('votes_count', 'upvotes_count', 'downvotes_count', 'comments_count', 'updated_on'))

    def vote(self, user, value=FEEDBACK_VOTE_UP):
        if user is None:
            return None
        from htk.apps.feedback.models import FeedbackRequestVote

        vote, _ = FeedbackRequestVote.objects.update_or_create(
            feedback=self,
            user=user,
            defaults={
                'value': value,
                'is_active': True,
                'is_spam': False,
            },
        )
        self.refresh_counts()
        return vote

    def upvote(self, user):
        return self.vote(user=user, value=FEEDBACK_VOTE_UP)

    def downvote(self, user):
        return self.vote(user=user, value=FEEDBACK_VOTE_DOWN)

    def unvote(self, user):
        if user is None:
            return 0
        count = self.votes.filter(user=user, is_active=True).update(is_active=False)
        self.refresh_counts()
        return count

    def json_encode(self):
        value = super(FeedbackRequest, self).json_encode()
        value.update(
            {
                'site_id': self.site_id,
                'request_type': self.request_type,
                'title': self.title,
                'description': self.description,
                'status': self.status,
                'visibility': self.visibility,
                'source_uri': self.source_uri,
                'votes_count': self.votes_count,
                'upvotes_count': self.upvotes_count,
                'downvotes_count': self.downvotes_count,
                'comments_count': self.comments_count,
                'is_hidden': self.is_hidden,
                'is_spam': self.is_spam,
                'needs_review': self.needs_review,
                'created_on': self.created_on,
                'updated_on': self.updated_on,
            }
        )
        return value
