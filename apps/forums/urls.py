# Django Imports
from django.urls import include
from django.urls import re_path
from django.views.decorators.cache import cache_page

# HTK Imports
import htk.apps.forums.views as views


urlpatterns = (
    re_path(r'^$', views.index, name='forum_index'),
    re_path(r'^(?P<fid>\d+)$', views.forum, name='forum'),
    re_path(r'^(?P<fid>\d+)/create$', views.thread_create, name='forum_thread_create'),
    re_path(r'^thread/(?P<tid>\d+)$', views.thread, name='forum_thread'),
    re_path(r'^thread/(?P<tid>\d+)/post$', views.message_create, name='forum_message_create'),
)
