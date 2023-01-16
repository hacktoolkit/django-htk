# Django Imports
from django.db import models

# HTK Imports
from htk.models.classes import HtkBaseModel
from htk.utils import utcnow


class AbstractToken(HtkBaseModel):
    key = models.CharField(max_length=255, unique=True)
    value = models.CharField(max_length=1023, blank=True)
    description = models.CharField(max_length=1023, blank=True)
    valid_after = models.DateTimeField(null=True, blank=True)
    valid_until = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True

    @property
    def is_valid(self):
        now = utcnow()

        is_valid = (self.valid_after is None or now >= self.valid_after) and (
            self.valid_until is None or now <= self.valid_until
        )

        return is_valid

    def enable(self):
        self.valid_after = utcnow()
        self.valid_until = None
        self.save()

    def disable(self):
        self.valid_after = None
        self.valid_until = utcnow()
        self.save()
