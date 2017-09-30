from django.contrib.sitemaps import Sitemap
from django.urls import reverse

from itertools import chain

# https://docs.djangoproject.com/en/1.8/ref/contrib/sitemaps/

class HtkBaseSitemap(Sitemap):
    priority = 0.5
    changefreq = 'daily'

    def get_static_view_names(self):
        static_view_names = []
        return static_view_names

    def get_model_instances(self):
        model_instances = []
        return model_instances

    def items(self):
        static_view_names = self.get_static_view_names()
        model_instances = self.get_model_instances()
        _items = list(chain(
            static_view_names,
            model_instances,
        ))
        return _items

    def location(self, obj):
        if type(obj) == str:
            path = reverse(obj)
        else:
            path = obj.get_absolute_url()
        return path
