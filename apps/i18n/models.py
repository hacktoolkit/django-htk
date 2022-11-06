# Django Imports
from django.db import models

# HTK Imports
from htk.apps.i18n.utils.choices import get_language_code_choices
from htk.models import HtkBaseModel
from htk.utils import htk_setting


class AbstractLocalizableString(HtkBaseModel):
    """A localizable string is a string that can be localized to a different language.

    It contains metadata about the string, but has no string representations itself.
    """

    key = models.CharField(max_length=128, unique=True)
    context = models.CharField(max_length=128, blank=True)
    description = models.CharField(max_length=256, blank=True)

    class Meta:
        abstract = True
        verbose_name = 'Localizable String'
        ordering = ('key',)

    def __str__(self):
        value = self.key
        return value

    def json_encode(self, include_key=True):
        value = {}
        if include_key:
            value.update(
                {
                    'key': self.key,
                }
            )

        value.update(
            {
                'translations': {
                    translation.language_code: translation.value
                    for translation in self.translations.order_by(
                        'language_code'
                    )
                },
            }
        )
        return value


class AbstractLocalizedString(HtkBaseModel):
    """A localized string is one that is associated with a localizable string, and has already been translated to a local language.

    The `language_code` is the ISO 639-1 language code combined with the ISO 3166-2 country code.

    See:
    - https://www.iso.org/iso-639-language-codes.html
    - https://en.wikipedia.org/wiki/ISO_639
    - https://en.wikipedia.org/wiki/ISO_639-1
    - https://en.wikipedia.org/wiki/List_of_ISO_639-1_codes
    - https://en.wikipedia.org/wiki/List_of_ISO_3166_country_codes

    Examples:
    - en-US - US English
    - en-UK - British English
    - zh-TW - Chinese Traditional (Taiwan)
    - zh-CN - Chinese Simplified (Mainland China)

    """

    localizable_string = models.ForeignKey(
        htk_setting('HTK_LOCALIZABLE_STRING_MODEL'),
        on_delete=models.CASCADE,
        related_name='translations',
    )
    language_code = models.CharField(
        max_length=5,
        choices=get_language_code_choices(),
        db_index=True,
    )  # '<ISO 639-1>-<ISO 3166-2>'
    value = models.TextField(max_length=512, blank=True)

    class Meta:
        abstract = True
        verbose_name = 'Localized String'
        ordering = (
            'localizable_string__key',
            'language_code',
        )

    def __str__(self):
        value = '{} - {}'.format(
            self.localizable_string.key, self.language_code
        )
        return value
