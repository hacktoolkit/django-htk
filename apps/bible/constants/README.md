# Bible Constants

## Overview

This module provides constants for Bible book metadata, aliases, and translation models. It includes comprehensive lists of all 66 canonical Bible books with chapter counts and common abbreviation mappings.

## Constants

### Books and Metadata

- **`BIBLE_BOOKS`** - List of all 66 canonical Bible book names
- **`BIBLE_BOOKS_DATA`** - List of dicts with book metadata: `name` and `chapters` count
- **`BIBLE_BOOKS_ALIASES`** - Dict mapping book names to lists of common abbreviations (e.g., 'Gen', 'Matt')
- **`BIBLE_BOOKS_ALIAS_MAPPINGS`** - Legacy dict mapping aliases and case variants to canonical book names
- **`resolve_bible_book_alias()`** - Resolves canonical book names, aliases, punctuation/spacing variants, and unambiguous prefixes to a canonical book name
- **`match_bible_book_alias()`** - Returns match metadata for exact, prefix, or optional fuzzy alias matches when the match is unique

### Model References

- **`HTK_BIBLE_BOOK_MODEL`** - Default: `'bible.BibleBook'`
- **`HTK_BIBLE_CHAPTER_MODEL`** - Default: `'bible.BibleChapter'`
- **`HTK_BIBLE_VERSE_MODEL`** - Default: `'bible.BibleVerse'`
- **`HTK_BIBLE_PASSAGE_MODEL`** - Default: `'bible.BiblePassage'`
- **`HTK_BIBLE_NASB_VERSE_MODEL`** - Default: `'bible.NASBVerse'`
- **`HTK_BIBLE_TRANSLATIONS_MAP`** - Dict mapping translation codes to model strings

## Enums

### BibleTestament

Bible division (Old Testament or New Testament):

```python
from htk.apps.bible.enums import BibleTestament

# Available testaments with values
BibleTestament.OT              # value: 1 (Old Testament)
BibleTestament.NT              # value: 2 (New Testament)

# Access enum properties
testament = BibleTestament.OT
print(f"{testament.name}: {testament.value}")  # OT: 1
```

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
from htk.apps.bible.utils.references import resolve_bible_book_alias

# Find canonical name from abbreviation, spacing/case variants, or safe prefix
canonical = resolve_bible_book_alias('Matt.')  # Returns 'Matthew'
canonical = resolve_bible_book_alias('I Jn')  # Returns '1 John'
canonical = resolve_bible_book_alias('Deu')  # Returns 'Deuteronomy'
ambiguous = resolve_bible_book_alias('Jo')  # Returns None
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
