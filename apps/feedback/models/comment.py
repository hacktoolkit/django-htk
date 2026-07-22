# Django Imports
from django.conf import settings
from django.db import models

# HTK Imports
from htk.apps.feedback.models.feedback import FeedbackRequest
from htk.models import HtkBaseModel


class FeedbackRequestComment(HtkBaseModel):
    feedback = models.ForeignKey(FeedbackRequest, related_name='comments', on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='feedback_request_comments', null=True, blank=True, default=None, on_delete=models.SET_DEFAULT)
    comment = models.TextField()
    is_internal = models.BooleanField(default=False)
    is_hidden = models.BooleanField(default=False)
    is_spam = models.BooleanField(default=False)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ('created_on',)
        verbose_name = 'Feedback request comment'
        verbose_name_plural = 'Feedback request comments'

    def __str__(self):
        return '%s comment on %s' % (self.user or 'Anonymous', self.feedback)

    def save(self, *args, **kwargs):
        super(FeedbackRequestComment, self).save(*args, **kwargs)
        self.feedback.refresh_counts()

    def json_encode(self):
        value = super(FeedbackRequestComment, self).json_encode()
        value.update(
            {
                'feedback_id': self.feedback_id,
                'comment': self.comment,
                'is_internal': self.is_internal,
                'created_on': self.created_on,
            }
        )
        return value
