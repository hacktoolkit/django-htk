# Django Imports
from django.urls import *

# HTK Imports
import htk.apps.feedback.views as views
from htk.apps.feedback.models import Feedback


urlpatterns = (
    re_path(r'^submit$', views.submit, name='htk_feedback_submit'),
)
