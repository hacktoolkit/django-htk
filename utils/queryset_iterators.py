DEFAULT_CHUNK_SIZE = 1000


def chunked_iterator(qs, size=DEFAULT_CHUNK_SIZE):
    qs = qs._clone()
    qs.query.clear_ordering(force_empty=True)
    qs.query.add_ordering('pk')
    last_pk = None
    empty = False
    while not empty:
        sub_qs = qs
        if last_pk:
            sub_qs = sub_qs.filter(pk__gt=last_pk)
        sub_qs = sub_qs[:size]
        empty = True
        for o in sub_qs:
            last_pk = o.pk
            empty = False
            yield o
