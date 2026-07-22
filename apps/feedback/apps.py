# Django Imports
from django.apps import AppConfig


class FeedbackConfig(AppConfig):
    default_auto_field = 'django.db.models.AutoField'
    name = 'htk.apps.feedback'
    label = 'feedback'
    verbose_name = 'Htk Feedback'
