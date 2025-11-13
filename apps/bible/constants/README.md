# Bible Constants

## Overview

This module provides constants for Bible book metadata, aliases, and translation models. It includes comprehensive lists of all 66 canonical Bible books with chapter counts and common abbreviation mappings.

## Constants

### Books and Metadata

- **`BIBLE_BOOKS`** - List of all 66 canonical Bible book names
- **`BIBLE_BOOKS_DATA`** - List of dicts with book metadata: `name` and `chapters` count
- **`BIBLE_BOOKS_ALIASES`** - Dict mapping book names to lists of common abbreviations (e.g., 'Gen', 'Matt')
- **`BIBLE_BOOKS_ALIAS_MAPPINGS`** - Dict mapping all aliases and case variants to canonical book names

### Model References

- **`HTK_BIBLE_BOOK_MODEL`** - Default: `'bible.BibleBook'`
- **`HTK_BIBLE_CHAPTER_MODEL`** - Default: `'bible.BibleChapter'`
- **`HTK_BIBLE_VERSE_MODEL`** - Default: `'bible.BibleVerse'`
- **`HTK_BIBLE_PASSAGE_MODEL`** - Default: `'bible.BiblePassage'`
- **`HTK_BIBLE_NASB_VERSE_MODEL`** - Default: `'bible.NASBVerse'`
- **`HTK_BIBLE_TRANSLATIONS_MAP`** - Dict mapping translation codes to model strings

## Usage Examples

### Access Book Information

```python
from htk.apps.bible.constants import BIBLE_BOOKS, BIBLE_BOOKS_DATA

# Get list of all book names
for book_name in BIBLE_BOOKS:
    print(book_name)  # Genesis, Exodus, ...

# Get book with chapter count
genesis = BIBLE_BOOKS_DATA[0]
print(f"{genesis['name']}: {genesis['chapters']} chapters")
```

### Resolve Book Aliases

```python
from htk.apps.bible.constants import BIBLE_BOOKS_ALIAS_MAPPINGS

# Find canonical name from abbreviation
canonical = BIBLE_BOOKS_ALIAS_MAPPINGS['Matt']  # Returns 'Matthew'
canonical = BIBLE_BOOKS_ALIAS_MAPPINGS['matt']  # Case-insensitive
```

### Configure Models

```python
# In Django settings.py
HTK_BIBLE_BOOK_MODEL = 'myapp.CustomBibleBook'
HTK_BIBLE_VERSE_MODEL = 'myapp.CustomVerse'
HTK_BIBLE_TRANSLATIONS_MAP = {
    'NASB': 'myapp.NASBVersion',
    'ESV': 'myapp.ESVVersion',
}
```
