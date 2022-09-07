# Python Standard Library Imports
import re


LOCALHOST_EMAILS = {
    'root@localhost',
}

ALL_BAD_EMAILS = LOCALHOST_EMAILS


BAD_EMAIL_REGEXPS = [
    re.compile(r'^.*@localhost$'),
]
