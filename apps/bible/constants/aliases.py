# Common Bible book abbreviations or aliases

BIBLE_BOOKS_ALIASES = {
    'Genesis' : [
        'Gen',
        'Gn',
    ],
    'Exodus' : [
        'Ex',
        'Exo',
    ],
    'Leviticus' : [
        'Lev',
        'Lv',
    ],
    'Numbers' : [
        'Num',
    ],
    'Deuteronomy' : [
        'Deut',
        'Dt',
    ],
    'Joshua' : [
        'Jos',
        'Josh',
    ],
    'Judges' : [
        'Jdg',
        'Judg',
        'Judge',
    ],
    'Ruth' : [
        'Rut',
    ],
    '1 Samuel' : [
        '1Sam',
        '1 Sam',
    ],
    '2 Samuel' : [
        '2Sam',
        '2 Sam',
    ],
    '1 Kings' : [
        '1Kin',
        '1 Kin',
    ],
    '2 Kings' : [
        '2Kin',
        '2 Kin',
    ],
    '1 Chronicles' : [
        '1Chr',
        '1 Chr',
    ],
    '2 Chronicles' : [
        '2Chr',
        '2 Chr',
    ],
    'Ezra' : [
        'Ezr',
    ],
    'Nehemiah' : [
        'Neh',
    ],
    'Esther' : [
        'Esth',
    ],
    'Job' : [
        'Job',
    ],
    'Psalms' : [
        'Ps',
        'Psalm',
    ],
    'Proverbs' : [
        'Pro',
        'Prov',
    ],
    'Ecclesiastes' : [
        'Eccl',
    ],
    'Song of Solomon' : [
        'Song',
        'Song of Songs',
        'Songs',
    ],
    'Isaiah' : [
        'Is',
        'Isa',
    ],
    'Jeremiah' : [
        'Jer',
    ],
    'Lamentations' : [
        'Lam',
    ],
    'Ezekiel' : [
        'Eze',
        'Ezek',
    ],
    'Daniel' : [
        'Dan',
    ],
    'Hosea' : [
        'Hos',
    ],
    'Joel' : [
        'Jl',
        'Joel',
    ],
    'Amos' : [
        'Am',
        'Amo',
        'Amos',
    ],
    'Obadiah' : [
        'Ob',
        'Oba',
        'Obad',
    ],
    'Jonah' : [
        'Jon',
    ],
    'Micah' : [
        'Mic',
    ],
    'Nahum' : [
        'Nah',
    ],
    'Habakkuk' : [
        'Hab',
    ],
    'Zephaniah' : [
        'Zep',
        'Zeph',
    ],
    'Haggai' : [
        'Hag',
    ],
    'Zechariah' : [
        'Zec',
        'Zech',
    ],
    'Malachi' : [
        'Mal',
    ],
    'Matthew' : [
        'Mat',
        'Matt',
    ],
    'Mark' : [
        'Mk',
    ],
    'Luke' : [
        'Luk',
    ],
    'John' : [
        'Jn',
    ],
    'Acts' : [
        'Act',
    ],
    'Romans' : [
        'Rom',
        'Roms',
    ],
    '1 Corinthians' : [
        '1Cor',
        '1 Cor',
        '1 Corin',
        '1 Corinth',
    ],
    '2 Corinthians' : [
        '2Cor',
        '2 Cor',
        '2 Corin',
        '2 Corinth',
    ],
    'Galatians' : [
        'Gal',
    ],
    'Ephesians' : [
        'Eph',
    ],
    'Philippians' : [
        'Phil',
    ],
    'Colossians' : [
        'Col',
        'Cols',
    ],
    '1 Thessalonians' : [
        '1Th',
        '1Thess',
        '1 Th',
        '1 Thess',
    ],
    '2 Thessalonians' : [
        '2Th',
        '2Thess',
        '2 Th',
        '2 Thess',
    ],
    '1 Timothy' : [
        '1Tim',
        '1 Tim',
    ],
    '2 Timothy' : [
        '2Tim',
        '2 Tim',
    ],
    'Titus' : [
        'Tit',
    ],
    'Philemon' : [
        'Philem',
        'Phlm',
        'Phm',
    ],
    'Hebrews' : [
        'Heb',
    ],
    'James' : [
        'Jam',
    ],
    '1 Peter' : [
        '1Pet',
        '1 Pet',
    ],
    '2 Peter' : [
        '2Pet',
        '2 Pet',
    ],
    '1 John' : [
        '1Jn',
        '1John',
        '1 Jn',
    ],
    '2 John' : [
        '2Jn',
        '2John',
        '2 Jn',
    ],
    '3 John' : [
        '3Jn',
        '3John',
        '3 Jn',
    ],
    'Jude' : [
        'Jud',
    ],
    'Revelation' : [
        'Rev',
    ],
}

# Programmatically build mappings from common Bible book abbreviations or aliases to canonical name, including uppercase and lowercase variants
BIBLE_BOOKS_ALIAS_MAPPINGS = {}

for book_name, aliases in BIBLE_BOOKS_ALIASES.iteritems():
    for alias in aliases:
        variants = (
            book_name.lower(),
            book_name.upper(),
            alias,
            alias.lower(),
            alias.upper(),
        )
        for variant in variants:
            BIBLE_BOOKS_ALIAS_MAPPINGS[variant] = book_name
