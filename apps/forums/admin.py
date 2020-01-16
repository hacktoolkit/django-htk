# Django Imports
from django.contrib import admin

# HTK Imports
from htk.apps.forums.models import Forum
from htk.apps.forums.models import ForumMessage
from htk.apps.forums.models import ForumTag
from htk.apps.forums.models import ForumThread


class ForumThreadInline(admin.TabularInline):
    model = ForumThread
    extra = 0

class ForumMessageInline(admin.TabularInline):
    model = ForumMessage
    extra = 0

class ForumAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'name',
        'description',
        'created',
        'updated',
    )
    inlines = [
        ForumThreadInline
    ]

class ForumThreadAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'forum',
        'subject',
        'author', 
        'created',
        'num_messages',
    )
    inlines = [
        ForumMessageInline,
    ]

class ForumMessageAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'thread',
        'snippet',
        'author',
        'timestamp',
    )

class ForumTagAdmin(admin.ModelAdmin):
    pass

admin.site.register(Forum, ForumAdmin)
admin.site.register(ForumThread, ForumThreadAdmin)
admin.site.register(ForumMessage, ForumMessageAdmin)
admin.site.register(ForumTag, ForumTagAdmin)
