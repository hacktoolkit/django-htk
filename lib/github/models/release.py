# Django Imports
from django.db import models
from django.utils.translation import gettext_lazy as _


class BaseRelease(models.Model):
    """Base model for GitHub releases.

    This abstract base class provides common fields and functionality for tracking
    GitHub releases. It can be inherited by specific release type models.
    """

    name = models.CharField(
        max_length=255,
        help_text=_("The title of the release"),
        blank=True,
    )
    repository = models.CharField(
        max_length=255,
        help_text=_("The name of the repository"),
    )
    tag_name = models.CharField(
        max_length=100,
        help_text=_("The name of the tag"),
        unique=True,
    )
    body = models.TextField(
        help_text=_("The description of the release"),
        blank=True,
    )
    draft = models.BooleanField(
        default=False,
        help_text=_("Whether this is a draft release"),
    )
    prerelease = models.BooleanField(
        default=False,
        help_text=_("Whether this is a prerelease"),
    )
    published_at = models.DateTimeField(
        help_text=_("The date and time when the release was published"),
        null=True,
        blank=True,
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        help_text=_("When this record was created"),
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        help_text=_("When this record was last updated"),
    )

    class Meta:
        abstract = True
        ordering = ["-version"]
        get_latest_by = "version"
        verbose_name = _("release")

    def __str__(self):
        """Return a string representation of the release."""
        return f"{self.tag_name}: {self.name or 'Untitled Release'}"

    @property
    def github_url(self):
        """Return the URL of the release."""
        return (
            f"https://github.com/{self.repository}/releases/tag/{self.tag_name}"
        )
