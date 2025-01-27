# Third Party (PyPI) Imports
from dataclasses import dataclass

# HTK Imports
from apps.features.utils import is_feature_enabled

# Django Imports
from django.conf import settings

# isort: off


@dataclass
class Feature:
    name: str
    label: str
    description: str

    @property
    def is_enabled(self):
        """Returns whether the feature is enabled."""
        return is_feature_enabled(self.name)

    def __str__(self):
        return self.name

    def __repr__(self):
        return f'<Feature: {self.name} ({self.label})>'

    def get_or_create(self):
        """Gets or creates the FeatureFlag instance for this feature."""
        module_path = f"{settings.PROJECT_NAME}.models"
        FeatureFlag = __import__(module_path, fromlist=['FeatureFlag']).FeatureFlag

        value = FeatureFlag.objects.get_or_create(
            name=self.name,
            # Correct usage of `get_or_create`. These defaults will only be used
            # while creating.
            defaults={
                'description': self.description,
                'enabled': False,
            },
        )
        return value

    def as_dict(self):

        return {
            'name': self.name,
            'is_enabled': self.is_enabled,
        }
