# Django Imports
from django.conf import settings
from django.db import models

# HTK Imports
from htk.apps.forums.constants.defaults import *
from htk.apps.forums.fk_fields import (
    fk_forum,
    fk_forum_thread,
)
from htk.models.fk_fields import fk_user


class Forum(models.Model):
    """Forum represents a message forum"""

    name = models.CharField(max_length=128)
    description = models.CharField(max_length=256, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        # app_label = 'htk'
        abstract = True

    def __str__(self):
        value = '%s' % (self.name,)
        return value

    @property
    def recent_thread(self):
        """Retrieves the most recent ForumThread"""
        thread = self.threads.order_by('-updated').first()
        return thread

    @property
    def num_threads(self) -> int:
        num = self.threads.count()
        return num

    @property
    def num_messages(self) -> int:
        total = sum(thread.num_messages for thread in self.threads.all())
        return total


class ForumThread(models.Model):
    forum = fk_forum(related_name='threads', required=True)
    subject = models.CharField(max_length=128)
    author = fk_user(related_name='authored_threads', required=False)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    # status
    sticky = models.BooleanField(default=False)
    closed = models.BooleanField(default=False)
    tags = models.ManyToManyField('ForumTag', blank=True)

    class Meta:
        # app_label = 'htk'
        abstract = True
        verbose_name = 'Forum Thread'

    def __str__(self):
        value = '%s - %s' % (
            self.forum,
            self.subject,
        )
        return value

    @property
    def num_messages(self):
        num = self.messages.count()
        return num

    @property
    def recent_message(self):
        """Retrieves the most recent message in ForumThread
        Requires all ForumThreads to have at least one message
        """
        message = self.messages.order_by('-timestamp').first()
        return message


class ForumMessage(models.Model):
    thread = fk_forum_thread(related_name='messages', required=True)
    author = fk_user(related_name='messages', required=True)
    reply_to = models.ForeignKey(
        'self',
        related_name='replies',
        blank=True,
        null=True,
        on_delete=models.CASCADE,
    )
    text = models.TextField(max_length=3000)
    posted_at = models.DateTimeField(auto_now_add=True)
    edited_at = models.DateTimeField(auto_now=True)
    tags = models.ManyToManyField('ForumTag', blank=True)

    class Meta:
        # app_label = 'htk'
        abstract = True
        verbose_name = 'Forum Message'

    def __str__(self):
        return 'ForumMessage %s' % (self.id,)

    @property
    def was_edited(self):
        return self.edited_at > self.posted_at

    @property
    def snippet(self):
        snippet = (
            (self.text[:FORUM_SNIPPET_LENGTH] + '...')
            if len(self.text) > FORUM_SNIPPET_LENGTH
            else self.text
        )
        return snippet

    def save(self, **kwargs):
        """Any customizations,  like updating cache, etc"""
        super(ForumMessage, self).save(**kwargs)
        # force update on `ForumThread.updated_at`
        self.thread.save()


class ForumTag(models.Model):
    """ForumTag can either apply to ForumThread or ForumMessage"""

    name = models.CharField(max_length=64)

    class Meta:
        # app_label = 'htk'
        abstract = True
        verbose_name = 'Forum Tag'

    def __str__(self):
        return self.name
