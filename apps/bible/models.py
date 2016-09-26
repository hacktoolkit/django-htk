from django.db import models

class AbstractBibleVerse(models.Model):
    """AbstractBibleVerse model
    """
    book = models.CharField(max_length=20)
    chapter = models.PositiveIntegerField()
    verse = models.PositiveIntegerField()

    class Meta:
        abstract = True
        verbose_name = 'Bible Verse'
        unique_together = (
            ('book', 'chapter', 'verse',),
        )

    def __unicode__(self):
        value = '%s %s:%s' % (self.book, self.chapter, self.verse,)
        return value

