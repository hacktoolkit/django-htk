# Django Imports
from django.db import models

# HTK Imports
from htk.models.classes import HtkBaseModel
from htk.utils import utcnow


class AbstractFeatureFlag(HtkBaseModel):
    name = models.CharField(max_length=255, unique=True)
    description = models.CharField(max_length=1023, blank=True)
    enabled = models.BooleanField(default=False)
    enabled_after = models.DateTimeField(null=True, blank=True)
    disabled_after = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True

    def as_dict(self):
        value = {
            'name': self.name,
            'description': self.description,
            'enabled': self.is_enabled,
            'enabled_after': self.enabled_after,
            'disabled_after': self.disabled_after,
        }
        return value

    def save(self, *args, **kwargs):
        super(AbstractFeatureFlag, self).save(*args, **kwargs)
        from htk.apps.features.utils import clear_cache
        clear_cache()

    @property
    def is_enabled(self):
        is_enabled = self.enabled

        if not is_enabled:
            if self.enabled_after is not None:
                now = utcnow()
                is_enabled = (
                    now >= self.enabled_after
                    and (
                        self.disabled_after is None
                        or now <= self.disabled_after
                    )
                )
            else:
                pass
        else:
            pass

        return is_enabled
