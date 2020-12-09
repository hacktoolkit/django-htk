# Django Imports
from django.contrib import admin
from django.utils.safestring import mark_safe


class HtkStoreProductAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'name',
        'description',
        'editor_notes',
        'amazon_product_id',
        'collections',
        'amazon_link',
    )

    def collections(self, obj):
        _collections = obj.collections.all()
        value = ', '.join([collection.name for collection in _collections])
        return value

    @mark_safe
    def amazon_link(self, obj):
        url = obj.get_amazon_url()
        link = '<a href="%s" target="_blank">Amazon Product URL</a>' % url
        return link
    amazon_link.allow_tags = True

class HtkStoreProductCollectionAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'name',
        'subtitle',
        'description',
    )
