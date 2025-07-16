# Django Imports
from django.db import models
from django.urls import reverse

# HTK Imports
from htk.apps import mp
from htk.lib.amazon.api import get_amazon_product_image_url
from htk.lib.amazon.utils import (
    build_amazon_ad_image_url,
    build_amazon_product_url,
    extract_asin_from_amazon_product_url,
)
from htk.models import HtkBaseModel
from htk.utils import htk_setting
from htk.utils.cache_descriptors import CachedAttribute
from htk.utils.text.transformers import seo_tokenize

from .fk_fields import fk_product_collection


# isort: off


class AbstractProduct(HtkBaseModel):
    name = models.CharField(max_length=128)
    description = models.TextField(max_length=1000, blank=True)
    editor_notes = models.TextField(max_length=1000, blank=True)
    # 3rd party
    amazon_product_id = models.CharField(max_length=64)

    # relationships
    collection = fk_product_collection(related_name='products')

    # meta
    timestamp = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True
        verbose_name = 'Product'

    def __str__(self):
        value = self.name
        return value

    @CachedAttribute
    def seo_title(self):
        title = '%s' % self.name
        seo_title = seo_tokenize(title, lower=True)
        return seo_title

    def get_absolute_url(self):
        url = reverse(
            'store_product',
            args=(
                self.id,
                self.seo_title,
            ),
        )
        return url

    # @mp.materialized_property(
    #     # DO NOT add `default=` parameter because it prevents this materialized
    #     # property from updating.
    #     models.CharField(max_length=64, null=True, blank=True),
    #     depends_on=['amazon_product_id'],
    #     dbl_check_on_post_save=True,
    # )
    # def asin(self):
    #     asin = extract_asin_from_amazon_product_url(self.amazon_product_id)
    #     return asin

    @property
    def amazon_tracking_id(self):
        # TODO: specify default
        amazon_tracking_id = htk_setting('HTK_AMAZON_TRACKING_ID')
        return amazon_tracking_id

    @property
    def amazon_url(self):
        base_url = build_amazon_product_url(self.amazon_product_id)
        url = f'{base_url}?&tag={self.amazon_tracking_id}'
        return url

    @property
    def amazon_image_url(self):
        # NOTE: First two methods not working
        # url = build_amazon_media_image_url(self.asin)
        url = build_amazon_ad_image_url(
            self.amazon_product_id, self.amazon_tracking_id
        )

        # url = get_amazon_product_image_url(self.amazon_product_id)
        return url

    ##
    # Legacy Methods for backwards compatibility

    def get_amazon_tracking_id(self):
        return self.amazon_tracking_id

    def get_amazon_url(self):
        return self.amazon_url

    def get_amazon_image_url(self):
        return self.amazon_image_url


class AbstractProductCollection(HtkBaseModel):
    name = models.CharField(max_length=128)
    subtitle = models.CharField(max_length=256)
    description = models.TextField(max_length=2000, blank=True)
    # NOTE: `products` as a `ManyToManyField` is for legacy purposes.
    # New apps should set define `HTK_STORE_PRODUCT_COLLECTION_MODEL` in Django settings.
    products = (
        models.ManyToManyField(
            htk_setting('HTK_STORE_PRODUCT_MODEL'),
            related_name='collections',
            blank=True,
        )
        if htk_setting('HTK_STORE_PRODUCT_COLLECTION_MODEL') is None
        else None
    )

    class Meta:
        abstract = True
        verbose_name = 'Product Collection'

    def __str__(self):
        return f'Product Collection: {self.name}'

    @CachedAttribute
    def seo_title(self):
        title = '%s' % self.name
        seo_title = seo_tokenize(title, lower=True)
        return seo_title

    def get_absolute_url(self):
        url = reverse(
            'store_collection',
            args=(
                self.id,
                self.seo_title,
            ),
        )
        return url

    @property
    def num_products(self):
        return self.products.count()
