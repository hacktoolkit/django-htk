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
