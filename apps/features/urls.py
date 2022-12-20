from django.conf.urls import url

import htk.apps.features.views as views

urlpatterns = [
    url(r'^$', views.features_view, name='htk_apps_features'),
    url(
        r'^(?P<fid>[0-9]+)/toggle$',
        views.features_toggle_view,
        name='htk_apps_features_toggle',
    ),
]
