# Django Imports
from django.conf.urls import *

# HTK Imports
import htk.apps.feedback.views as views
from htk.apps.feedback.models import Feedback


urlpatterns = (
    url(r'^submit$', views.submit, name='htk_feedback_submit'),
)
