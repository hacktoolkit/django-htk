# Bible App

Scripture data and Bible reference tools.

## Quick Start

```python
from htk.apps.bible.models import (
    AbstractBibleBook,
    AbstractBibleChapter,
    AbstractBibleVerse,
    AbstractBiblePassage
)

# Create book
book = AbstractBibleBook.objects.create(name='Genesis', abbreviation='Gen')

# Create chapter
chapter = AbstractBibleChapter.objects.create(book=book, number=1)

# Create verses
verse = AbstractBibleVerse.objects.create(
    chapter=chapter,
    number=1,
    text='In the beginning God created the heavens and the earth.'
)

# Create passage (multiple verses)
passage = AbstractBiblePassage.objects.create(
    book=book,
    chapter_start=1,
    verse_start=1,
    chapter_end=1,
    verse_end=3
)
```

## Common Patterns

```python
# Get scripture references
from htk.apps.bible.utils.references import get_scripture_references_compact

refs = get_scripture_references_compact('John 3:16')

# Query verses
john = AbstractBibleBook.objects.get(abbreviation='John')
chapter3 = john.chapters.get(number=3)
verse16 = chapter3.verses.get(number=16)
```

## Models

- **`AbstractBibleBook`** - Books of the Bible
- **`AbstractBibleChapter`** - Chapters within books
- **`AbstractBibleVerse`** - Individual verses
- **`AbstractBiblePassage`** - Multiple verses/passages

## Related Modules

- `htk.lib.esv` - ESV Bible API integration
- `htk.lib.songselect` - Worship song database
