from django.urls import re_path

from htk.apps.admintools import views

urlpatterns = [
    re_path(r'^(.*?)?$', views.admintools_view, name='admintools'),
]
