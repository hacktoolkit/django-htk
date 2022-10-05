# Django Imports
from django.apps import AppConfig
from django.db.models import signals

# HTK Imports
from htk.app_config import HtkAppConfig


class HtkBibleAppConfig(HtkAppConfig):
    name = 'htk.apps.bible'
    label = 'bible'
    verbose_name = 'Bible'

    def ready(self):
        pass
