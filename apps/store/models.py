from django.db import models

from htk.utils import htk_setting

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
