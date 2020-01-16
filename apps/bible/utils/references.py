# Python Standard Library Imports



def get_scripture_references_list(bible_passages):
    scripture_references = ['%s' % bible_passage for bible_passage in bible_passages]
    return scripture_references


def get_scripture_references_str(bible_passages):
    scripture_references = get_scripture_references_list(bible_passages)
    scripture_references_str = '; '.join(scripture_references)
    return scripture_references_str


def get_scripture_references_compact(bible_passages):
    # TODO
    """Returns a nested list of scripture references

    Input: 'Psalm 119:9,11' (bible passages str representation)

    Output: [
        {
            'book' : 'Psalms',
            'passages' : [
                {
                    'chapter' : 119,
                    'verses' : [9, 11,],
                },
            ],
        },
    ]

    """
    scripture_references_compact = []

    prev_book = None
    prev_chapter = None

    book_passages = None
    chapter_verses = None

    for bible_passage in bible_passages:
        book = bible_passage.book
        chapter = bible_passage.chapter_start

        if book != prev_book:
            book_passages = []

        if chapter != prev_chapter:
            chapter_verses = []

        prev_book = book
        prev_chapter = prev_chapter

    return scripture_references_compact


def get_scripture_references_str_compact(bible_passages):
    # TODO
    scripture_references_compact = get_scripture_references_compact(bible_passages)
    return ';'.join(scripture_references_compact)
