from django.conf.urls import *

from htk.apps.feedback.models import Feedback
import htk.apps.feedback.views as views

urlpatterns = (
    url(r'^submit$', views.submit, name='htk_feedback_submit'),
)
