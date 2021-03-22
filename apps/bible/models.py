# Python Standard Library Imports
import re

# Django Imports
from django.db import models

# HTK Imports
from htk.apps.bible.utils import (
    get_bible_book_choices,
    get_bible_book_model,
    get_bible_chapter_model,
    get_translation_model,
)
from htk.utils import htk_setting


# isort: off


class AbstractBibleBook(models.Model):
    """AbstractBibleBook model

    66 Books of the Bible
    """
    name = models.CharField(max_length=20, unique=True)
    testament = models.PositiveIntegerField(choices=get_bible_book_choices())

    class Meta:
        abstract = True
        verbose_name = 'Bible Book'
        ordering = (
            'id',
        )

    def __str__(self):
        value = '%s' % self.name
        return value

    @classmethod
    def from_reference(cls, reference):
        from htk.apps.bible.constants.aliases import BIBLE_BOOKS_ALIAS_MAPPINGS

        book_name = BIBLE_BOOKS_ALIAS_MAPPINGS.get(reference, reference)
        try:
            book = cls.objects.get(name=book_name)
        except cls.DoesNotExist:
            book = None
        return book


class AbstractBibleChapter(models.Model):
    """AbstractBibleChapter model
    """
    book = models.ForeignKey(htk_setting('HTK_BIBLE_BOOK_MODEL'), on_delete=models.CASCADE, related_name='chapters')
    chapter = models.PositiveIntegerField()

    class Meta:
        abstract = True
        verbose_name = 'Bible Chapter'
        unique_together = (
            ('book', 'chapter',),
        )
        ordering = (
            'book',
            'chapter',
        )

    def __str__(self):
        value = '%s %s' % (self.book.name, self.chapter,)
        return value


class AbstractBibleVerse(models.Model):
    """AbstractBibleVerse model
    """
    book = models.ForeignKey(htk_setting('HTK_BIBLE_BOOK_MODEL'), on_delete=models.CASCADE, related_name='%(class)ss')
    chapter = models.ForeignKey(htk_setting('HTK_BIBLE_CHAPTER_MODEL'), on_delete=models.CASCADE, related_name='%(class)ss')
    verse = models.PositiveIntegerField()

    class Meta:
        abstract = True
        verbose_name = 'Bible Verse'
        unique_together = (
            ('book', 'chapter', 'verse',),
        )
        ordering = (
            'book',
            'chapter',
            'verse',
        )

    def __str__(self):
        value = '%s %s:%s' % (self.book.name, self.chapter.chapter, self.verse,)
        return value

    def as_dict(self):
        value = {
            'ref': str(self),
            'book': self.book.name,
            'chapter': self.chapter.chapter,
            'verse': self.verse,
        }
        return value

    def get_translation(self, translation):
        translation_model = get_translation_model(translation)
        if translation_model:
            verse = translation_model.objects.get(
                book=self.book,
                chapter=self.chapter,
                verse=self.verse
            )
        else:
            verse = None
        return verse


class AbstractBiblePassage(models.Model):
    """AbstractBiblePassage model

    For Bible passage citations
    """
    book = models.ForeignKey(htk_setting('HTK_BIBLE_BOOK_MODEL'), on_delete=models.CASCADE, related_name='passages')
    chapter_start = models.ForeignKey(htk_setting('HTK_BIBLE_CHAPTER_MODEL'), on_delete=models.CASCADE, related_name='passages_start')
    verse_start = models.PositiveIntegerField(null=True, blank=True)
    chapter_end = models.ForeignKey(htk_setting('HTK_BIBLE_CHAPTER_MODEL'), on_delete=models.CASCADE, null=True, blank=True, related_name='passages_end')
    verse_end = models.PositiveIntegerField(null=True, blank=True)

    class Meta:
        abstract = True
        verbose_name = 'Bible Verse'
        unique_together = (
            ('book', 'chapter_start', 'verse_start', 'chapter_end', 'verse_end',),
        )
        ordering = (
            'book',
            'chapter_start',
            'verse_start',
            'chapter_end',
            'verse_end',
        )

    def __str__(self):
        ends_in_different_chapter = self.chapter_end is not None and self.chapter_end != self.chapter_start

        value = '%(book)s %(chapter_start)s%(verse_start_separator)s%(verse_start)s%(separator)s%(chapter_end)s%(verse_end_separator)s%(verse_end)s' % {
            'book': self.book.name,
            'chapter_start': self.chapter_start.chapter,
            'verse_start_separator': ':' if self.verse_start else '',
            'verse_start': self.verse_start if self.verse_start else '',
            'separator': '-' if self.chapter_end else '',
            'chapter_end': self.chapter_end.chapter if ends_in_different_chapter else '',
            'verse_end_separator': ':' if ends_in_different_chapter and self.verse_end else '',
            'verse_end': self.verse_end if self.verse_end else '',
        }

        return value

    def as_dict(self, translation=None):
        value = {
            'version': translation,
            'ref': str(self),
            'verses': [verse.as_dict() for verse in self.verses(translation=translation)],
        }
        return value

    @classmethod
    def from_reference(cls, reference, persist=False):
        pattern = r'^(?P<book_name>.+) (?P<chapter_start>\d+)(?P<verse_start_separator>:?)(?P<verse_start>\d*)(?P<separator>-?)(?P<chapter_end>\d*)(?P<verse_end_separator>:?)(?P<verse_end>\d*)$'

        match = re.match(pattern, reference)
        if match:
            book_name = match.group('book_name')
            chapter_start = match.group('chapter_start')
            verse_start_separator = match.group('verse_start_separator')
            verse_start = match.group('verse_start')
            verse_start = int(verse_start) if verse_start else None
            separator = match.group('separator')
            chapter_end = match.group('chapter_end')
            chapter_end = int(chapter_end) if chapter_end else None
            verse_end_separator = match.group('verse_end_separator')
            verse_end = match.group('verse_end')
            verse_end = int(verse_end) if verse_end else None

            if verse_end is None:
                # verse_end is missing
                # determine if another part was captured as verse_end

                if chapter_end:
                    if verse_start:
                        # chapter_end is actually verse_end for same passage that starts and ends in the same chapter
                        verse_end = chapter_end
                        chapter_end = chapter_start
                    else:
                        # reference is an entire Bible chapter
                        pass
                else:
                    # there is no chapter_end either, do nothing
                    pass
            else:
                # there is a verse_end, do nothing
                pass

            BibleBook = get_bible_book_model()
            BibleChapter = get_bible_chapter_model()

            book = BibleBook.from_reference(book_name)
            chapter_start_obj = BibleChapter.objects.get(
                book=book,
                chapter=chapter_start
            )
            if chapter_end:
                chapter_end_obj = BibleChapter.objects.get(
                    book=book,
                    chapter=chapter_end
                )
            elif verse_end:
                chapter_end_obj = chapter_start_obj
            else:
                chapter_end_obj = None

            if persist:
                bible_passage, was_created = cls.objects.get_or_create(
                    book=book,
                    chapter_start=chapter_start_obj,
                    verse_start=verse_start,
                    chapter_end=chapter_end_obj,
                    verse_end=verse_end
                )
            else:
                bible_passage = cls(
                    book=book,
                    chapter_start=chapter_start_obj,
                    verse_start=verse_start,
                    chapter_end=chapter_end_obj,
                    verse_end=verse_end
                )
        else:
            bible_passage = None

        return bible_passage

    def verses(self, translation=None):
        if self.chapter_end is None:
            verses = self.chapter_start.bibleverses.all()

            if self.verse_start is not None:
                verses = verses.filter(
                    verse=self.verse_start
                )
        elif self.chapter_end == self.chapter_start:
            verses = self.chapter_start.bibleverses.filter(
                verse__gte=self.verse_start,
                verse__lte=self.verse_end
            )
        elif self.chapter_end != self.chapter_start:
            if self.chapter_end.chapter < self.chapter_start.chapter:
                raise Except('Bad passage reference')

            verses = []

            verses__chapter_start = self.chapter_start.bibleverses.all()
            if self.verse_start is not None:
                verses__chapter_start = verses__chapter_start.filter(
                    verse__gte=self.verse_start
                )

            verses__chapter_between = [
                verse
                for chapter in self.book.chapters.filter(
                    chapter__gt=self.chapter_start.chapter,
                    chapter__lt=self.chapter_end.chapter
                )
                for verse in chapter.bibleverses.all()
            ]

            verses__chapter_end = self.chapter_end.bibleverses.all()
            if self.verse_end is not None:
                verses__chapter_end = verses__chapter_end.filter(
                    verse__lte=self.verse_end
                )

            verses.extend(list(verses__chapter_start))
            verses.extend(verses__chapter_between)
            verses.extend(list(verses__chapter_end))
        else:
            # impossible case
            verses = []

        if translation:
            verses = [verse.get_translation(translation) for verse in verses]

        return verses
