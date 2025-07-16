# Django Imports
from django.contrib import admin
from django.utils.safestring import mark_safe

# HTK Imports
from htk.utils import (
    htk_setting,
    resolve_model_dynamically,
)


class HtkStoreProductAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'name',
        'description',
        'editor_notes',
        'amazon_product_id',
        # 'asin',
        'collections',
        'amazon_link',
    )

    @admin.display(description='Collection(s)')
    def collections(self, obj):
        if hasattr(obj, 'collections'):
            _collections = obj.collections.all()
            value = ', '.join([collection.name for collection in _collections])
        else:
            value = obj.collection
        return value

    @mark_safe
    def amazon_link(self, obj):
        url = obj.get_amazon_url()
        link = '<a href="%s" target="_blank">Amazon Product URL</a>' % url
        return link

    amazon_link.allow_tags = True


class HtkStoreProductInline(admin.TabularInline):
    model = resolve_model_dynamically(htk_setting('HTK_STORE_PRODUCT_MODEL'))
    extra = 0
    can_delete = True


class HtkStoreProductCollectionAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'name',
        'subtitle',
        'description',
    )

    inlines = (HtkStoreProductInline,)
