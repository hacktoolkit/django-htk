# Django Imports
from django.apps import AppConfig
from django.db.models import signals


class HtkOrganizationAppConfig(AppConfig):
    name = 'htk.apps.organizations'
    label = 'organizations'
    verbose_name = 'Organizations'

    def ready(self):
        pass
