# HTK Imports
from htk.utils import htk_setting
from htk.utils.general import resolve_model_dynamically


def get_translation_model(translation):
    translations_map = htk_setting('HTK_BIBLE_TRANSLATIONS_MAP')
    translation_model_class = translations_map.get(translation.upper())
    translation_model = (
        resolve_model_dynamically(translation_model_class)
        if translation_model_class
        else None
    )
    return translation_model
