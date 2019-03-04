 # Python Standard Library Imports

# Third Party / PIP Imports

# Django Imports


# HTK Imports
from htk.utils.enums import get_enum_choices


def get_bible_book_choices():
    from htk.apps.bible.enums import BibleTestament
    choices = get_enum_choices(BibleTestament)
    return choices
