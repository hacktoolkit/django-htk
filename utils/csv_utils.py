import cStringIO
import codecs
import csv

class UTF8Recoder(object):
    """
    Iterator that reads an encoded stream and reencodes the input to UTF-8

    https://docs.python.org/2/library/csv.html
    """
    def __init__(self, f, encoding):
        self.reader = codecs.getreader(encoding)(f)

    def __iter__(self):
        return self

    def next(self):
        return self.reader.next().encode('utf-8')

class UnicodeReader(object):
    """
    A CSV reader which will iterate over lines in the CSV file "f",
    which is encoded in the given encoding.

    https://docs.python.org/2/library/csv.html
    """

    def __init__(self, f, dialect=csv.excel, encoding='utf-8', **kwds):
        f = UTF8Recoder(f, encoding)
        self.reader = csv.reader(f, dialect=dialect, **kwds)

    def next(self):
        row = self.reader.next()
        return [unicode(s, 'utf-8') for s in row]

    def __iter__(self):
        return self

class UnicodeWriter(object):
    """
    A CSV writer which will write rows to CSV file "f",
    which is encoded in the given encoding.

    https://docs.python.org/2/library/csv.html
    """

    def __init__(self, f, dialect=csv.excel, encoding='utf-8', **kwds):
        # Redirect output to a queue
        self.queue = cStringIO.StringIO()
        self.writer = csv.writer(self.queue, dialect=dialect, **kwds)
        self.stream = f
        self.encoder = codecs.getincrementalencoder(encoding)()

    def writerow(self, row):
        self.writer.writerow([s.encode('utf-8') for s in row])
        # Fetch UTF-8 output from the queue ...
        data = self.queue.getvalue()
        data = data.decode('utf-8')
        # ... and reencode it into the target encoding
        data = self.encoder.encode(data)
        # write to the target stream
        self.stream.write(data)
        # empty queue
        self.queue.truncate(0)

    def writerows(self, rows):
        for row in rows:
            self.writerow(row)

def buffered_csv_from_collection(f, collection, row_generator, headings=None, utf8=True):
    """Buffers CSV to the stream `f`
    """
    # get csv writer
    if utf8:
        writer = UnicodeWriter(f)
    else:
        writer = csv.writer(f)
    # write the column headings
    if headings:
        writer.writerow(headings)
    for item in collection:
        writer.writerow(row_generator(item))

def get_csv_stringbuf_from_collection(collection, row_generator, headings=None, utf8=True):
    buf = cStringIO.StringIO()
    buffered_csv_from_collection(buf, collection, row_generator, headings=headings, utf8=utf8)
    return buf

def get_csv_response_from_collection(collection, row_generator, headings=None, filename='data.csv', utf8=True):
    from django.http import HttpResponse
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="%s"' % filename
    buffered_csv_from_collection(response, collection, row_generator, headings=headings, utf8=utf8)
    return response
