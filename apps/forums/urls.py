# Django Imports
from django.conf.urls import include
from django.conf.urls import url
from django.views.decorators.cache import cache_page

# HTK Imports
import htk.apps.forums.views as views


urlpatterns = (
    url(r'^$', views.index, name='forum_index'),
    url(r'^(?P<fid>\d+)$', views.forum, name='forum'),
    url(r'^(?P<fid>\d+)/create$', views.thread_create, name='forum_thread_create'),
    url(r'^thread/(?P<tid>\d+)$', views.thread, name='forum_thread'),
    url(r'^thread/(?P<tid>\d+)/post$', views.message_create, name='forum_message_create'),
)
