# Django Imports
from django.contrib import admin

# HTK Imports
from htk.utils import htk_setting
from htk.utils.general import resolve_model_dynamically


Conversation = resolve_model_dynamically(htk_setting('HTK_CONVERSATION_MODEL'))
ConversationMessage = resolve_model_dynamically(
    htk_setting('HTK_CONVERSATION_MESSAGE_MODEL')
)
ConversationMessageReaction = resolve_model_dynamically(
    htk_setting('HTK_CONVERSATION_MESSAGE_REACTION_MODEL')
)
ConversationParticipant = resolve_model_dynamically(
    htk_setting('HTK_CONVERSATION_PARTICIPANT_MODEL')
)


class ConversationParticipantInline(admin.TabularInline):
    model = ConversationParticipant
    extra = 0


class ConversationMessageInline(admin.TabularInline):
    model = ConversationMessage
    extra = 0


class BaseConversationAdmin(admin.ModelAdmin):
    model = Conversation

    list_display = (
        'id',
        'topic',
        'description',
        'num_participants',
        'num_messages',
        'created_by',
        'created_at',
        'updated_at',
    )

    inlines = (
        ConversationParticipantInline,
        # NOTE: This will crash if the there are too many messages in the conversation
        ConversationMessageInline,
    )

    search_fields = (
        'topic',
        'description',
        'created_by__username',
        'created_by__first_name',
        'created_by__last_name',
    )


class BaseConversationParticipantAdmin(admin.ModelAdmin):
    model = ConversationParticipant

    list_display = (
        'id',
        'conversation',
        'user',
        'joined_at',
    )

    search_fields = (
        'conversation__topic',
        'user__username',
        'user__first_name',
        'user__last_name',
    )

    list_filters = (
        'conversation',
        'user',
    )


class BaseConversationMessageAdmin(admin.ModelAdmin):
    model = ConversationMessage

    list_display = (
        'id',
        'conversation',
        'author',
        'reply_to',
        'content',
        'posted_at',
        'edited_at',
        'deleted_at',
    )


class BaseConversationMessageReactionAdmin(admin.ModelAdmin):
    model = ConversationMessageReaction

    list_display = (
        'id',
        'message',
        'created_at',
        'emoji',
    )
