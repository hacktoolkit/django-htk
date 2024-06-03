# Python Standard Library Imports
import re
import unicodedata

# Third Party (PyPI) Imports
import emoji


def is_emoji_symbol(s: str) -> bool:
    return emoji.emoji_count(s) > 0


def is_emoji_shortcode(s: str) -> bool:
    return (
        bool(re.match(r'^:.*:$', s)) and emoji.emojize(s, language='alias') != s
    )


def demojize(s: str, shortest=True) -> str:
    """Strips emojis from a string"""
    demojized = emoji.demojize(s)
    aliases = re.findall(r':\w+?:', demojized)
    if aliases:
        # Return the shortest alias
        return min(aliases, key=len)
    return demojized


def unicode_to_ascii(s):
    """Converts a Unicode string to ASCII equivalent if possible
    http://en.wikipedia.org/wiki/Canonical_decomposition#Normalization
    """
    s = s.replace('\u2019', "'")
    ascii_s = (
        unicodedata.normalize('NFKD', s)
        .encode('ascii', 'ignore')
        .decode('utf-8')
    )
    return ascii_s
