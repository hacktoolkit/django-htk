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
    book = models.ForeignKey(htk_setting('HTK_BIBLE_BOOK_MODEL'))
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
    book = models.ForeignKey(htk_setting('HTK_BIBLE_BOOK_MODEL'))
    chapter = models.ForeignKey(htk_setting('HTK_BIBLE_CHAPTER_MODEL'))
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
