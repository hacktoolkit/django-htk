# Python Standard Library Imports
import re

# HTK Imports
from htk.compat import IS_PYTHON_2
from htk.utils.text.constants import SUMMARY_NUM_SENTENCES
from htk.utils.text.general import (
    is_ascii,
    is_ascii_extended,
)
from htk.utils.text.regexes import SEO_TOKEN_INVALID_CHARS_REGEX
from htk.utils.text.unicode import unicode_to_ascii


def get_symbols(sentence, valid_chars='A-Za-z0-9_-'):
    """Returns a list of symbols from a sentence

    By default, these are considered valid characters for a symbol:
    - letters (A-Z, a-z)
    - numbers (0-9)
    - underscore (_)
    - hyphen (-)
    """
    invalid_chars = re.compile(r'[^%s]' % valid_chars)
    symbols = [symbol for symbol in invalid_chars.split(sentence) if symbol]
    return symbols


def get_sentences(paragraph):
    """Returns a list of sentences from a paragraph

    This is a rather naive implementation; there are probably better ones out there
    Assumes that the paragraph has proper punctuation.
    """
    punctuation = re.compile(r'[\.!?]')
    sentences = [sentence.strip() for sentence in punctuation.split(paragraph)]
    sentences = list(filter(lambda x: x, sentences))
    return sentences


def summarize(paragraph, num_sentences=SUMMARY_NUM_SENTENCES):
    """Returns a summary of a paragraph

    This is a naive implementation and does not use advanced NLP techniques

    `paragraph` is one big long string
    `num_sentences` the number of sentences desired in the summary

    TODO: produce a more faithful summary. This currently converts any terminal punctuation ([\.!?]) to periods (.)
    """
    sentences = get_sentences(paragraph)
    paragraph_num_sentences = len(sentences)
    limit = min(paragraph_num_sentences, num_sentences)
    summary_sentences = sentences[:limit]
    if paragraph_num_sentences < num_sentences:
        # the original was already short enough, so just display the original
        summary = paragraph
    else:
        if not paragraph_num_sentences:
            # empty paragraph
            summary = ''
        else:
            # we actually summarized it
            summary = '.'.join(summary_sentences) + '...'
    return summary


def ellipsize(text, max_len=100, truncate=False):
    """
    Cut `text` off at `max_len` characters, inserting an ellipsis at the appropriate point so that
    the total length is at or below the max.

    Attempts to break on a word boundary.

    Algorithm based on https://github.com/mvhenten/ellipsize/blob/master/index.js

    `truncate` whether we may truncate long words if there were no breaks
      Defaults to `False`

      e.g.
      ellipsize('abcdefghijklmnop', max_len=6, truncate=True) -> 'abc...'
      ellipsize('abcdefghijklmnop', max_len=6, truncate=False) -> ''
    """
    if not text:
        return ''

    if IS_PYTHON_2:
        text = unicode(text)  # noqa F401
    text_len = len(text)

    if text_len <= max_len:
        return text

    boundary_chars = (
        ' ',
        '-',
    )
    ellipsis = '...'
    max_len = max_len - len(ellipsis)

    last_break = 0  # store candidate index for break point
    for i in range(text_len):
        c = text[i]
        if c in boundary_chars:
            last_break = i

        if i < max_len:
            continue
        else:
            # time to shorten the string
            if last_break == 0:
                if truncate:
                    text = text[:max_len] + ellipsis
                else:
                    text = ''
            else:
                text = text[:last_break] + ellipsis
            break

    return text


def seo_tokenize(
    title, lower=True, preserve_ascii_extended=False, preserve_unicode=False
):
    """Get SEO-tokenized version of a string, typically a name or title

    `title` the string to tokenize
    `lower` whether to lowercase the string
    `preserve_ascii_extended` will preserve extended ASCII characters if `True`
    `preserve_unicode` will preserve Unicode if `True`
    e.g.
    <- "The World's Greatest Establishment"
    -> 'the-worlds-greatest-establishment'

    <- 'Recreational Sports Facility, Berkeley, CA', lower=False
    -> 'Recreational-Sports-Facility-Berkeley-CA'
    """
    tokens = SEO_TOKEN_INVALID_CHARS_REGEX.split(title.strip())
    cleaned_title = ' '.join(tokens)

    try:
        if preserve_ascii_extended or preserve_unicode:
            # do nothing, keep extended ASCII and Unicode in title
            pass
        else:
            cleaned_title = unicode_to_ascii(cleaned_title)
    except Exception:
        pass

    if lower:
        cleaned_title = cleaned_title.lower()
    else:
        pass

    def _repl(matchobj):
        c = matchobj.group(0)
        if is_ascii_extended(c):
            replaced_c = c if preserve_ascii_extended else ''
        elif is_ascii(c):
            # it is ASCII, but not one of the accepted ASCII characters
            replaced_c = ''
        else:
            replaced_c = c if preserve_unicode else ''
        return replaced_c

    cleaned_title = re.sub(r'[^ \-A-Za-z0-9]', _repl, cleaned_title)

    # replace whitespace in string with hyphens
    tokenized_title = '-'.join(cleaned_title.split())

    return tokenized_title


def snake_case_to_camel_case(s):
    """Convert `snake_case` string to `CamelCase`"""
    camel_string = ''.join(part.capitalize() for part in s.lower().split('_'))
    return camel_string


def snake_case_to_lower_camel_case(s):
    """Convert `snake_case` string to `camelCase`"""
    camel_string = snake_case_to_camel_case(s)
    camel_string = camel_string[0].lower() + camel_string[1:]
    return camel_string


def pascal_case_to_snake_case(s):
    """Convert `PascalCase` string to `snake_case`"""
    snake_string = ''.join(
        ['_' + c.lower() if c.isupper() else c for c in s]
    ).lstrip('_')
    return snake_string
