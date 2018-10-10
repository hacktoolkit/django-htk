"""Utilities for formatting Python objects as English phrases and sentences
"""

def oxford_comma(items):
    """Given a list of items, properly comma and 'and' them together

    Expects `items` to be a list of strings
    """
    result = ''

    if len(items) == 0:
        result = ''
    elif len(items) == 1:
        result = items[0]
    elif len(items) == 2:
        result = ' and '.join(items)
    elif len(items) > 2:
        result = ', and '.join([', '.join(items[:-1]), items[-1],])
    else:
        raise Exception('oxford_comma: Illegal arguments')

    return result
