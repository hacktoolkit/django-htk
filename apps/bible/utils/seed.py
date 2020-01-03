 # Python Standard Library Imports

# Third Party / PIP Imports

# Django Imports

# HTK Imports
from htk.apps.bible.constants import BIBLE_BOOKS
from htk.apps.bible.constants import BIBLE_BOOKS_DATA
from htk.apps.bible.enums import BibleTestament
from htk.apps.bible.utils import get_all_chapters
from htk.apps.bible.utils import get_bible_book_model
from htk.apps.bible.utils import get_bible_chapter_model


def seed_bible():
    seed_bible_books()
    seed_bible_chapters()


def seed_bible_books():
    BibleBook = get_bible_book_model()
    count = 0
    for book_name in BIBLE_BOOKS:
        testament = BibleTestament.OT if count < 39 else BibleTestament.NT
        book = BibleBook.objects.create(
            name=book_name,
            testament=testament.value
        )
        count += 1


def seed_bible_chapters():
    BibleBook = get_bible_book_model()
    BibleChapter = get_bible_chapter_model()

    for book_data in BIBLE_BOOKS_DATA:
        book = BibleBook.objects.get(name=book_data['name'])
        for i in range(book_data['chapters']):
            chapter = BibleChapter.objects.create(
                book=book,
                chapter=i + 1
            )
