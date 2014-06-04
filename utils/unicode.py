import unicodedata

def unicode_to_ascii(str):
    """Converts a Unicode string to ASCII equivalent if possible
    http://en.wikipedia.org/wiki/Canonical_decomposition#Normalization
    """
    ascii = unicodedata.normalize('NFKD', str).encode('ascii', 'ignore')
    return ascii
