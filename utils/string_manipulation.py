import re

from htk.utils.constants import *

def get_sentences(paragraph):
    """Returns a list of sentences from a paragraph

    This is a rather naive implementation; there are probably better ones out there
    Assumes that the paragraph has proper punctuation.
    """
    punctuation = re.compile(r'[\.!?]')
    sentences = [sentence.strip() for sentence in punctuation.split(paragraph)]
    sentences = filter(lambda x: x, sentences)
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
        if not(paragraph_num_sentences):
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

    text = unicode(text)
    text_len = len(text)

    if text_len <= max_len:
        return text

    boundary_chars = (
        ' ',
        '-',
    )
    ellipsis = '...'
    max_len = max_len - len(ellipsis)

    last_break = 0 # store candidate index for break point
    for i in xrange(text_len):
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
