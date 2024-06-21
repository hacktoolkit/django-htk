# Django Imports
from django.contrib import admin

# HTK Imports
from htk.utils import htk_setting
from htk.utils.general import resolve_model_dynamically


Forum = resolve_model_dynamically(htk_setting('HTK_FORUM_MODEL'))
ForumThread = resolve_model_dynamically(htk_setting('HTK_FORUM_THREAD_MODEL'))
ForumMessage = resolve_model_dynamically(htk_setting('HTK_FORUM_MESSAGE_MODEL'))
ForumTag = resolve_model_dynamically(htk_setting('HTK_FORUM_TAG_MODEL'))


class ForumThreadInline(admin.TabularInline):
    model = ForumThread
    extra = 0


class ForumMessageInline(admin.TabularInline):
    model = ForumMessage
    extra = 0


class ForumAdmin(admin.ModelAdmin):
    model = Forum

    list_display = (
        'id',
        'name',
        'description',
        'created_at',
        'updated_at',
    )
    inlines = (ForumThreadInline,)


class ForumThreadAdmin(admin.ModelAdmin):
    model = ForumThread

    list_display = (
        'id',
        'forum',
        'subject',
        'author',
        'created',
        'num_messages',
    )
    inlines = (ForumMessageInline,)

    # search_fields = (
    #     'forum',
    #     'subject',
    #     'author',
    #     'created',
    #     'num_messages',
    # )


class ForumMessageAdmin(admin.ModelAdmin):
    model = ForumMessage

    list_display = (
        'id',
        'thread',
        'snippet',
        'author',
        'posted_at',
    )


class ForumTagAdmin(admin.ModelAdmin):
    model = ForumTag

    list_display = (
        'id',
        'name',
    )


# admin.site.register(Forum, ForumAdmin)
# admin.site.register(ForumThread, ForumThreadAdmin)
# admin.site.register(ForumMessage, ForumMessageAdmin)
# admin.site.register(ForumTag, ForumTagAdmin)
