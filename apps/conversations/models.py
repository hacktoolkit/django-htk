# Third Party (PyPI) Imports
import emoji

# Django Imports
from django.db import models

# HTK Imports
from htk.apps.conversations.fk_fields import (
    fk_conversation,
    fk_conversation_message,
)
from htk.models.fk_fields import fk_user
from htk.utils import htk_setting
from htk.utils.text.unicode import (
    demojize,
    is_emoji_shortcode,
    is_emoji_symbol,
)


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

    @classmethod
    def find_all_by_user(cls, user):
        """Finds all conversations that a user is a participant in"""
        conversations = cls.objects.filter(participants__user=user).distinct()
        return conversations

    @classmethod
    def find_by_participants(cls, participants):
        """Finds a conversation by participants

        This is useful for finding an existing conversation between a set of participants
        """

        participant_ids = set([participant.id for participant in participants])
        num_participants = len(participant_ids)

        conversation = (
            cls.objects.annotate(
                n_participants=models.Count('participants'),
                n_user_matches=models.Count(
                    'participants',
                    filter=models.Q(participants__user_id__in=participant_ids),
                ),
            )
            .filter(
                n_participants=num_participants,
                n_user_matches=num_participants,
            )
            .first()
        )

        return conversation

    @property
    def num_participants(self):
        num = self.participants.count()
        return num

    @property
    def num_messages(self):
        num = self.messages.count()
        return num

    def add_participant(self, user):
        """Adds a participant to this conversation"""
        self.participants.get_or_create(user=user)

    def add_participants(self, users):
        """Adds several participants to this conversation"""
        for user in users:
            self.add_participant(user)


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

    def add_reaction(self, user, emoji_shortcode):
        """Adds a reaction by `user` to this message.

        This method is idempotent. If it is called multiple times with the same arguments, it will only create 1 record of the emoji reaction.
        """
        if is_emoji_symbol(emoji_shortcode):
            # ensure that data is normalized into emoji shortcode
            emoji_shortcode = emoji.demojize(emoji_shortcode)

        self.reactions.get_or_create(
            user=user,
            emoji_shortcode=emoji_shortcode,
        )

    def remove_reaction(self, user, emoji_shortcode):
        """Removes an existing reaction by `user` to this message.

        This method is idempotent. If it is called multiple times with the same arguments, it will remove the record of the emoji reaction.

        If it is called multiple times, and the reaction has already been deleted, this method has no effect and just performs a no-op.
        """
        if is_emoji_symbol(emoji_shortcode):
            # ensure that data is normalized into emoji shortcode
            emoji_shortcode = emoji.demojize(emoji_shortcode)

        self.reactions.filter(
            user=user,
            emoji_shortcode=emoji_shortcode,
        ).delete()

    def save(self, **kwargs):
        """Saves this message.

        Side effect: also performs any customizations, like updating cache, etc
        """
        super().save(**kwargs)

        # force update on `Conversation.updated_at`
        self.conversation.save()


class BaseConversationMessageReaction(models.Model):
    """An emoji reaction to a message in
    a conversation.
    """

    message = fk_conversation_message(related_name='reactions', required=True)
    user = fk_user(related_name='reactions', required=False)
    emoji_shortcode = models.CharField(max_length=24)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        abstract = True

    def __str__(self):
        value = '%s' % emoji.emojize(self.emoji_shortcode)
        return value

    def repair_emoji(self):
        """Repairs the emoji shortcode to ensure that it is normalized."""
        if is_emoji_shortcode(self.emoji_shortcode):
            # normalize into emoji symbol
            self.emoji_shortcode = emoji.emojize(self.emoji_shortcode)
            self.save()

        if is_emoji_symbol(self.emoji_shortcode):
            # normalize into emoji shortcode
            self.emoji_shortcode = demojize(self.emoji_shortcode)
            self.save()
