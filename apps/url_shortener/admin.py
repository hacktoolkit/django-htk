from django.contrib import admin

from htk.apps.url_shortener.models import HTKShortUrl
from htk.apps.url_shortener.models import HTKShortUrlAccess
from htk.utils import htk_setting

class HTKShortUrlAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'url',
        'creator',
        'created_on',
        'code',
        'prepared_id',
        'link',
        'access_count',
    )

    def code(self, obj):
        return obj.get_code()

    def prepared_id(self, obj):
        return obj.get_prepared_id()

    def link(self, obj):
        uri = obj.get_short_uri()
        shortened_link = '<a href="%(uri)s" target="_blank">%(uri)s</a>' % {
            'uri' : uri,
        }
        return shortened_link
    link.allow_tags = True

    def access_count(self, obj):
        count = obj.get_access_count()
        return count

class HTKShortUrlAccessAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'long_url',
        'short_url',
        'timestamp',
        'user',
        'user_agent',
        'user_ip',
        'referrer',
    )

    def long_url(self, obj):
        return obj.url

    def short_url(self, obj):
        return obj.url.get_short_uri()

admin.site.register(HTKShortUrl, HTKShortUrlAdmin)
admin.site.register(HTKShortUrlAccess, HTKShortUrlAccessAdmin)
