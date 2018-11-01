import unicodedata

def unicode_to_ascii(s):
    """Converts a Unicode string to ASCII equivalent if possible
    http://en.wikipedia.org/wiki/Canonical_decomposition#Normalization
    """
    s = s.replace(u'\u2019', "'")
    ascii = unicodedata.normalize('NFKD', s).encode('ascii', 'ignore')
    return ascii
