from django.urls import re_path, include

from htk.apps.admintools import views

urlpatterns = [
    re_path(
        r'^api/app_config$', views.app_config, name='admintools_app_config'
    ),
    re_path(r'^pages/', include('htk.apps.admintools.pages.urls')),
    # This MUST be last
    re_path(r'^(.*?)?$', views.admintools_view, name='admintools'),
]
