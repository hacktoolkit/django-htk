import re

from htk.utils.text.unicode import unicode_to_ascii

def ssml_sanitized(s):
    sanitized = re.sub(r'&', 'and', unicode_to_ascii(s))
    return sanitized


