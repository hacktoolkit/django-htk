# Django Imports
from django.urls import *

# HTK Imports
import htk.apps.feedback.views as views
from htk.apps.feedback.models import Feedback


urlpatterns = (
    re_path(r'^submit$', views.submit, name='htk_feedback_submit'),
    re_path(r'^requests$', views.request_list, name='htk_feedback_request_list'),
    re_path(r'^requests/matches$', views.request_matches, name='htk_feedback_request_matches'),
    re_path(r'^requests/my$', views.request_my, name='htk_feedback_request_my'),
    re_path(r'^requests/submit$', views.request_submit, name='htk_feedback_request_submit'),
    re_path(r'^requests/(?P<request_id>\d+)$', views.request_detail, name='htk_feedback_request_detail'),
    re_path(r'^requests/(?P<request_id>\d+)/vote$', views.request_vote, name='htk_feedback_request_vote'),
    re_path(r'^requests/(?P<request_id>\d+)/unvote$', views.request_unvote, name='htk_feedback_request_unvote'),
    re_path(r'^requests/(?P<request_id>\d+)/comment$', views.request_comment, name='htk_feedback_request_comment'),
    re_path(r'^requests/(?P<request_id>\d+)/status$', views.request_status_update, name='htk_feedback_request_status_update'),
)
