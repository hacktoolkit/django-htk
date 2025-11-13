# HTK Bible Utils

Utilities for Bible data management including scripture lookups, references, seeding, and translations.

## Functions by Category

### Model Getters (4 functions)

**get_bible_book_model()**
- Resolves HTK_BIBLE_BOOK_MODEL setting
- Returns BibleBook model class

**get_bible_chapter_model()**
- Resolves HTK_BIBLE_CHAPTER_MODEL setting
- Returns BibleChapter model class

**get_bible_verse_model()**
- Resolves HTK_BIBLE_VERSE_MODEL setting
- Returns BibleVerse model class

**get_bible_passage_model()**
- Resolves HTK_BIBLE_PASSAGE_MODEL setting
- Returns BiblePassage model class

### Lookup Functions (5 functions)

**lookup_bible_verse(book, chapter, verse)**
- Looks up a specific verse by book name, chapter number, and verse number
- Returns BibleVerse object or None if not found

**resolve_bible_passage_reference(reference)**
- Resolves string reference to BiblePassage object
- Calls BiblePassage.from_reference() for parsing
- Returns BiblePassage or None

**resolve_bible_verse_reference(reference)**
- Parses reference string format: "Book Chapter:Verse"
- Uses regex pattern matching
- Returns BibleVerse or None

**get_bible_chapter_data(book, chapter)**
- Gets chapter metadata for book and chapter number
- Returns dict with 'num_verses' key

**get_all_chapters()**
- Gets all Bible chapters as formatted strings
- Format: "BookName ChapterNumber"
- Returns list based on BIBLE_BOOKS_DATA constant

### Reference Functions (4 functions)

**get_scripture_references_list(bible_passages)**
- Converts BiblePassage objects to string list
- Returns list of formatted scripture references

**get_scripture_references_str(bible_passages)**
- Joins scripture references with semicolon separator
- Returns formatted string: "Psalm 119:9; John 3:16"

**get_scripture_references_compact(bible_passages)**
- Converts passages to nested structure (implementation in progress)
- Organizes by book, then chapter, then verses
- Returns list of dicts with book/chapter/verses structure

**get_scripture_references_str_compact(bible_passages)**
- Joins compact scripture references (implementation in progress)
- Returns semicolon-joined string

### Seeding Functions (3 functions)

**seed_bible()**
- Seeds complete Bible data
- Calls seed_bible_books() then seed_bible_chapters()

**seed_bible_books()**
- Creates BibleBook objects for all 66 books
- Automatically assigns Old Testament (OT) vs New Testament (NT)
- Uses BIBLE_BOOKS constant for all book names

**seed_bible_chapters()**
- Creates BibleChapter objects for all chapters
- Creates appropriate number of chapters per book
- Uses BIBLE_BOOKS_DATA constant for chapter counts

### Translation Functions (1 function)

**get_translation_model(translation)**
- Looks up translation model from HTK_BIBLE_TRANSLATIONS_MAP setting
- Translation name is uppercased for lookup
- Returns model class or None if not found

### Choice Functions (1 function)

**get_bible_book_choices()**
- Gets enum choices from BibleTestament enum
- Returns list of (value, name) tuples for form choices

## Example Usage

```python
from htk.apps.bible.utils import (
    lookup_bible_verse,
    get_scripture_references_str,
    seed_bible,
)

# Lookup a verse
verse = lookup_bible_verse('John', 3, 16)

# Format multiple passages
passages = [...]  # BiblePassage objects
ref_str = get_scripture_references_str(passages)

# Seed Bible data
seed_bible()
```
