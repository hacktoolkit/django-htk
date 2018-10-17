"""Utilities for formatting Python objects as English phrases and sentences
"""

def oxford_comma(items, conjunction='and'):
    """Given a list of items, properly comma and 'and' or 'or' them together

    Expects `items` to be a list of strings
    """
    result = ''

    if len(items) == 0:
        result = ''
    elif len(items) == 1:
        result = items[0]
    elif len(items) == 2:
        result = (' %s ' % conjunction).join(items)
    elif len(items) > 2:
        result = (', %s ' % conjunction).join([', '.join(items[:-1]), items[-1],])
    else:
        raise Exception('oxford_comma: Illegal arguments')

    return result
