# Django Imports
from django.conf import settings
from django.db import models

# HTK Imports
from htk.apps.forums.constants import *


class Forum(models.Model):
    """Forum represents a message forum
    """
    name = models.CharField(max_length=64)
    description = models.CharField(max_length=128, blank=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        app_label = 'htk'

    def __str__(self):
        value = '%s' % (
            self.name,
        )
        return value

    def recent_thread(self):
        """Retrieves the most recent ForumThread
        """
        ordered_threads = self.threads.order_by('-updated')
        if len(ordered_threads):
            thread = ordered_threads[0]
        else:
            thread = None
        return thread

    def num_threads(self):
        num = self.threads.count()
        return num

    def num_messages(self):
        num = 0
        for thread in self.threads.all():
            num += thread.num_messages()
        return num

class ForumThread(models.Model):
    forum = models.ForeignKey(Forum, related_name='threads')
    subject = models.CharField(max_length=128)
    author = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='authored_threads')
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    # status
    sticky = models.BooleanField(default=False)
    closed = models.BooleanField(default=False)
    tags = models.ManyToManyField('ForumTag', blank=True)

    class Meta:
        app_label = 'htk'
        verbose_name = 'Forum Thread'

    def __str__(self):
        value = '%s - %s' % (
            self.forum,
            self.subject,
        )
        return value

    def num_messages(self):
        num = self.messages.count()
        return num

    def recent_message(self):
        """Retrieves the most recent message in ForumThread
        Requires all ForumThreads to have at least one message
        """
        ordered_messages = self.messages.order_by('-timestamp')
        if len(ordered_messages):
            message = ordered_messages[0]
        else:
            message = None
        return message

class ForumMessage(models.Model):
    thread = models.ForeignKey(ForumThread, related_name='messages')
    author = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='messages')
    text = models.TextField(max_length=3000)
    timestamp = models.DateTimeField(auto_now=True)
    tags = models.ManyToManyField('ForumTag', blank=True)

    class Meta:
        app_label = 'htk'
        verbose_name = 'Forum Message'

    def __str__(self):
        return 'ForumMessage %s' % (self.id,)

    def snippet(self):
        snippet = (self.text[:FORUM_SNIPPET_LENGTH] + '...') if len(self.text) > FORUM_SNIPPET_LENGTH else self.text
        return snippet

    def save(self, **kwargs):
        """Any customizations,  like updating cache, etc
        """
        super(ForumMessage, self).save(**kwargs)
        self.thread.save() # update ForumThread.updated timestamp

class ForumTag(models.Model):
    """ForumTag can either apply to ForumThread or ForumMessage
    """
    name = models.CharField(max_length=32)

    class Meta:
        app_label = 'htk'
        verbose_name = 'Forum Tag'

    def __str__(self):
        return self.name
