# Django Imports
from django.apps import AppConfig

# HTK Imports
from htk.apps.mp.services import prepare_handlers


class MpApp(AppConfig):
    name = 'htk.apps.mp'

    def ready(self):
        for handler in prepare_handlers:
            handler()
