# Python Standard Library Imports
import copy
import re
import time

# HTK Imports
from htk.constants.dns import COMMON_TLDS
from htk.constants.emails import COMMON_EMAIL_HANDLES
from htk.constants.emails.bad import (
    ALL_BAD_EMAILS,
    BAD_EMAIL_REGEXPS,
)
from htk.constants.emails.permutations import EMAIL_PERMUTATION_PATTERNS
from htk.utils import (
    htk_setting,
    resolve_method_dynamically,
)


# isort: off


def is_bad_email(email):

    is_bad = email in ALL_BAD_EMAILS

    if not is_bad:
        for pattern in BAD_EMAIL_REGEXPS:
            if pattern.match(email) is not None:
                is_bad = True
                break

    return is_bad


def normalize_email(email):
    normalized = email.strip().lower()
    return normalized


def email_permutator(domain, first_name='', middle_name='', last_name=''):
    """Generate common possible permutations of emails given company `domain` and `*_name`
    """
    domain = domain.lower()
    first_name = first_name.lower()
    middle_name = middle_name.lower()
    last_name = last_name.lower()
    parts = {
        'fn' : first_name,
        'fi' : first_name[0] if first_name else '',
        'mn' : middle_name,
        'mi' : middle_name[0] if middle_name else '',
        'ln' : last_name,
        'li' : last_name[0] if last_name else '',
        'domain' : domain,
    }

    email_possibilities = []
    email_patterns = copy.copy(EMAIL_PERMUTATION_PATTERNS)
    for email_pattern in email_patterns:
        base = email_pattern.replace('{', '%(').replace('}', ')s') + '@%(domain)s'
        email_possibility = base % parts
        email_possibilities.append(email_possibility)

    # filter out empty middle name emails
    bad_email_re = re.compile(r'^.*(\.\.|--|__).*$')
    email_permutations = filter(lambda x: bad_email_re.match(x) is None, list(set(email_possibilities)))
    return email_permutations


def find_company_emails_for_name(domain, first_name='', middle_name='', last_name=''):
    """Find a list of emails for a `domain` and `*_name` combination
    """
    email_permutations = email_permutator(
        domain,
        first_name=first_name,
        middle_name=middle_name,
        last_name=last_name
    )
    find_valid_emails = resolve_method_dynamically(htk_setting('HTK_FIND_EMAILS_VALIDATOR'))
    emails = find_valid_emails(email_permutations)
    return emails


def extract_snowflake_handle_from_email(email):
    """Extracts a handle from an email address that will likely be unique
    """
    handle, domain = email.split('@')
    if handle in COMMON_EMAIL_HANDLES:
        domain_prefix, tld = domain.rsplit('.', 1)
        if tld in COMMON_TLDS:
            handle = domain_prefix
        else:
            handle = domain
    return handle
