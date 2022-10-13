"""Utilities for formatting Python objects as English phrases and sentences
"""

# HTK Imports
from htk.constants.i18n.en import SPECIAL_NOUN_PLURAL_FORMS


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


def pluralize_noun(noun, count):
    """Adds 's' to `noun` depending on `count`
    """
    use_plural_form = count == 0 or count > 1  # pluralize 0 or many; 1 is singular

    if use_plural_form:
        if noun in SPECIAL_NOUN_PLURAL_FORMS:
            trimmed_noun = SPECIAL_NOUN_PLURAL_FORMS[noun]
            suffix = ''
        elif len(noun) > 3 and noun[-3:] == 'sis':
            # e.g. analysis, basis, crisis, diagnosis, oasis, synopsis, thesis
            trimmed_noun = noun[:-3]
            suffix = 'ses'
        elif len(noun) > 2 and noun[-2:] in ('on', 'um'):
            # e.g. addendum, bacterium, criterion, curriculum, medium, phenomenon, phyla
            trimmed_noun = noun[:-2]
            suffix = 'a'
        elif len(noun) > 2 and noun[-2:] in ('ex', 'ix'):
            # e.g. appendix, codex, index, matrix
            trimmed_noun = noun[:-2]
            suffix = 'ices'
        elif len(noun) > 2 and noun[-2:] == 'us':
            # e.g. alumnus, bacillus, cactus, fungus, octopus, syllabus
            trimmed_noun = noun[:-2]
            suffix = 'i'
        elif len(noun) > 2 and noun[-2:] == 'fe':
            # e.g. knife, wife
            trimmed_noun = noun[:-2]
            suffix = 'ves'
        elif noun[-1] == 'f':
            # e.g. shelf, wolf
            trimmed_noun = noun[:-1]
            suffix = 'ves'
        elif noun[-1] == 'a':
            # e.g. alumna, formula
            trimmed_noun = noun
            suffix = 'e'
        elif noun[-1] == 'y':
            # e.g. candy
            trimmed_noun = noun[:-1]
            suffix = 'ies'
        elif noun[-1] == 's':
            # e.g. class
            trimmed_noun = noun
            suffix = 'es'
        else:
            trimmed_noun = noun
            suffix = 's'
    else:
        trimmed_noun = noun
        suffix = ''

    pluralized = trimmed_noun + suffix
    return pluralized


def pluralize_verb(verb, n_subjects):
    """Adds 's' to `verb` for singular `n_subjects`
    """
    if verb in ('is', 'are',):
        pluralized = pluralize_verb__tobe(n_subjects)
    else:
        suffix = 's' if n_subjects == 1 else ''
        pluralized = verb + suffix

    return pluralized


def pluralize_verb__tobe(n_subjects):
    pluralized = 'is' if n_subjects == 1 else 'are'
    return pluralized
