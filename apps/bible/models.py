 # Python Standard Library Imports

# Third Party / PIP Imports

# Django Imports
from django.db import models

# HTK Imports
from htk.apps.bible.utils import get_bible_book_choices
from htk.utils import htk_setting


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

    def __unicode__(self):
        value = u'%s' % self.name
        return value


class AbstractBibleChapter(models.Model):
    """AbstractBibleChapter model
    """
    book = models.ForeignKey(htk_setting('HTK_BIBLE_BOOK_MODEL'), related_name='chapters')
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

    def __unicode__(self):
        value = u'%s %s' % (self.book.name, self.chapter,)
        return value


class AbstractBibleVerse(models.Model):
    """AbstractBibleVerse model
    """
    book = models.ForeignKey(htk_setting('HTK_BIBLE_BOOK_MODEL'), related_name='%(class)ss')
    chapter = models.ForeignKey(htk_setting('HTK_BIBLE_CHAPTER_MODEL'), related_name='%(class)ss')
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

    def __unicode__(self):
        value = '%s %s:%s' % (self.book.name, self.chapter.chapter, self.verse,)
        return value


class AbstractBiblePassage(models.Model):
    """AbstractBiblePassage model

    For Bible passage citations
    """
    book = models.ForeignKey(htk_setting('HTK_BIBLE_BOOK_MODEL'), related_name='passages')
    chapter_start = models.ForeignKey(htk_setting('HTK_BIBLE_CHAPTER_MODEL'), related_name='passages_start')
    verse_start = models.PositiveIntegerField(null=True, blank=True)
    chapter_end = models.ForeignKey(htk_setting('HTK_BIBLE_CHAPTER_MODEL'), null=True, blank=True, related_name='passages_end')
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

    def __unicode__(self):
        ends_in_different_chapter = self.chapter_end is not None and self.chapter_end != self.chapter_start

        value = '%(book)s %(chapter_start)s%(verse_start_separator)s%(verse_start)s%(separator)s%(chapter_end)s%(verse_end_separator)s%(verse_end)s' % {
            'book' : self.book.name,
            'chapter_start' : self.chapter_start.chapter,
            'verse_start_separator' : ':' if self.verse_start else '',
            'verse_start' : self.verse_start if self.verse_start else '',
            'separator' : '-' if self.chapter_end else '',
            'chapter_end' : self.chapter_end.chapter if ends_in_different_chapter else '',
            'verse_end_separator' : ':' if ends_in_different_chapter and self.verse_end else '',
            'verse_end' : self.verse_end if self.verse_end else '',
        }

        return value
