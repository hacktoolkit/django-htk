# Django Imports
from django.db import models

# HTK Imports
from htk.apps.conversations.fk_fields import fk_conversation
from htk.models.fk_fields import fk_user
from htk.utils import htk_setting


# isort: off


class BaseConversation(models.Model):
    """A base conversation class which is extensible

    A conversation is a collection of messages between `n` participants, where `n >= 2`.

    When `n` is:
    - `2`, it is a private conversation, or a direct message ("DM")
    - `>2`, it is a group conversation
    """

    topic = models.CharField(max_length=256, blank=True)
    description = models.TextField(max_length=1024, blank=True)
    created_by = fk_user(related_name='created_conversations', required=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True

    def __str__(self):
        value = '%s (#%s)' % (
            self.topic or '<No Topic>',
            self.id,
        )
        return value

    @property
    def num_participants(self):
        num = self.participants.count()
        return num

    @property
    def num_messages(self):
        num = self.messages.count()
        return num


class BaseConversationParticipant(models.Model):
    """A participant in a conversation

    This is a many-to-many relationship between a User and a Conversation
    For n-party conversations, there will be n-1 ConversationParticipants
    """

    conversation = fk_conversation(related_name='participants', required=True)
    user = fk_user(related_name='conversation_participants', required=True)
    joined_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        abstract = True

    def __str__(self):
        value = '%s - %s' % (
            self.conversation,
            self.user,
        )
        return value


class BaseConversationMessage(models.Model):
    """A message in a conversation

    A conversation message is a message that belongs to a conversation.

    A conversation message is visible to all participants in the conversation.
    """

    conversation = fk_conversation(related_name='messages', required=True)
    # `author` is not required when the message is system-generated
    author = fk_user(
        related_name='authored_conversation_messages', required=False
    )
    reply_to = models.ForeignKey(
        'self',
        related_name='replies',
        blank=True,
        null=True,
        on_delete=models.CASCADE,
    )
    content = models.TextField(
        max_length=htk_setting('HTK_CONVERSATION_MESSAGE_MAX_LENGTH')
    )
    posted_at = models.DateTimeField(auto_now_add=True)
    edited_at = models.DateTimeField(blank=True, null=True)
    # soft-deletion: app will hide messages that are "deleted"; but also allow for messages to be "undeleted"
    deleted_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        abstract = True

    def __str__(self):
        value = '%s - %s' % (
            self.conversation,
            self.author,
        )
        return value

    @property
    def was_edited(self):
        return self.edited_at is not None and self.edited_at > self.posted_at

    @property
    def is_deleted(self):
        return self.deleted_at is not None

    def save(self, **kwargs):
        """Saves this message.

        Side effect: also performs any customizations, like updating cache, etc
        """
        super().save(**kwargs)

        # force update on `Conversation.updated_at`
        self.conversation.save()
