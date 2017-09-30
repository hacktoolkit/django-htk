import jsonfield

from django.conf import settings
from django.db import models
from django.urls import reverse

from htk.utils import utcnow
from htk.utils.data_structures import *
from htk.utils.request import build_dict_from_request
from htk.utils.request import get_current_request

class HTKShortUrl(models.Model):
    """
    Short URL code is traditionally duosexagesimal (base 62)
    C.f. http://en.wikipedia.org/wiki/List_of_numeral_systems
    
    62 ** 3 = 238,328
    62 ** 4 = 14,776,336
    62 ** 5 = 916,132,832
    62 ** 6 = 56,800,235,584

    Freemium model
    - Custom domain accounts would be able to have any-length codes
    - Premium accounts would be able to have shorter codes
    - Free accounts would have longer codes (6)
    """
    url = models.CharField(max_length=256)
    creator = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='short_urls', blank=True, null=True, default=None, on_delete=models.SET_DEFAULT)
    created_on = models.DateTimeField(auto_now_add=True)

    class Meta:
        app_label = 'htk'
        verbose_name = 'Short URL'

    def __unicode__(self):
        value = self.url
        return value

    def get_code(self):
        from htk.apps.url_shortener.utils import generate_short_url_code
        code = generate_short_url_code(self.id)
        return code

    def get_prepared_id(self):
        from htk.apps.url_shortener.utils import pre_encode
        prepared_id = pre_encode(self.id)
        return prepared_id

    def get_short_uri(self, domain=None):
        if domain is None:
            request = get_current_request()
            domain = request.get_host() if request else htk_setting('HTK_CANONICAL_DOMAIN')
        else:
            pass
        uri = 'http://%s%s' % (
            domain,
            reverse('shorturl', args=(self.get_code(),)),
        )
        return uri

    def record_request(self, request):
        keys = (
            'user',
            'user_agent',
            'user_ip',
            'referrer',
        )
        metadata = filter_dict(
            build_dict_from_request(request),
            keys
        )
        
        access = HTKShortUrlAccess.objects.create(
            url=self,
            **metadata
        )

    def get_access_count(self):
        count = self.accesses.count()
        return count

class HTKShortUrlAccess(models.Model):
    url = models.ForeignKey('htk.HTKShortUrl', related_name='accesses')
    timestamp = models.DateTimeField(auto_now=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, blank=True, null=True, default=None, on_delete=models.SET_DEFAULT)
    user_agent = models.CharField(max_length=256, blank=True)
    user_ip = models.CharField(max_length=15, blank=True)
    referrer = models.CharField(max_length=256, blank=True)

    class Meta:
        app_label = 'htk'
        verbose_name = 'Short URL Access Log'
