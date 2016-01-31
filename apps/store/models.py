from django.core.urlresolvers import reverse
from django.db import models

from htk.utils import htk_setting
from htk.utils.text.transformers import seo_tokenize

class AbstractProduct(models.Model):
    name = models.CharField(max_length=128)
    description = models.TextField(max_length=1000, blank=True)
    editor_notes = models.TextField(max_length=1000, blank=True)
    # 3rd party
    amazon_product_id = models.CharField(max_length=64)

    # meta
    timestamp = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True

    def __unicode__(self):
        value = self.name
        return value

    def get_seo_title(self):
        title = '%s' % self.name
        seo_title = seo_tokenize(title, lower=True)
        return seo_title

    def get_absolute_url(self):
        seo_title = self.get_seo_title()
        url = reverse('store_product', args=(self.id, seo_title,))
        return url

    def get_amazon_tracking_id(self):
        # TODO: specify default
        amazon_tracking_id = htk_setting('HTK_AMAZON_TRACKING_ID')
        return amazon_tracking_id

    def get_amazon_url(self):
        url = 'http://www.amazon.com/gp/product/%(amazon_product_id)s/ref=as_li_tl?ie=UTF8&camp=1789&creative=390957&creativeASIN=%(amazon_product_id)s&linkCode=as2&tag=%(amazon_tracking_id)s' % {
            'amazon_product_id' : self.amazon_product_id,
            'amazon_tracking_id' : self.get_amazon_tracking_id(),
        }
        return url

    def get_amazon_image_url(self):
        url = 'http://ws-na.amazon-adsystem.com/widgets/q?_encoding=UTF8&ASIN=%(amazon_product_id)s&Format=_SL250_&ID=AsinImage&MarketPlace=US&ServiceVersion=20070822&WS=1&tag=%(amazon_tracking_id)s'  % {
            'amazon_product_id' : self.amazon_product_id,
            'amazon_tracking_id' : self.get_amazon_tracking_id(),
        }
        return url

class AbstractProductCollection(models.Model):
    name = models.CharField(max_length=128)
    subtitle = models.CharField(max_length=256)
    description = models.TextField(max_length=2000, blank=True)
    products = models.ManyToManyField(htk_setting('HTK_STORE_PRODUCT_MODEL'), related_name='collections', blank=True)

    class Meta:
        abstract = True

    def get_seo_title(self):
        title = '%s' % self.name
        seo_title = seo_tokenize(title, lower=True)
        return seo_title

    def get_absolute_url(self):
        seo_title = self.get_seo_title()
        url = reverse('store_collection', args=(self.id, seo_title,))
        return url
