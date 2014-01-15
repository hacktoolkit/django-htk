from django.conf.urls import *

from htk.apps.feedback.models import Feedback
import htk.apps.feedback.views as views

urlpatterns = patterns(
    '',
    url(r'^submit$', views.submit, name='htk_feedback_submit'),
)
