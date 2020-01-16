# Python Standard Library Imports
import unicodedata


def unicode_to_ascii(s):
    """Converts a Unicode string to ASCII equivalent if possible
    http://en.wikipedia.org/wiki/Canonical_decomposition#Normalization
    """
    s = s.replace('\u2019', "'")
    ascii_s = unicodedata.normalize('NFKD', s).encode('ascii', 'ignore').decode('utf-8')
    return ascii_s
