# HTK Imports
from htk.constants.geo import *


def get_us_state_abbreviation_choices(include_blank=True):
    choices = [('', '--')] if include_blank else []
    for state in US_STATES:
        abbrev = state['abbrev']
        choices.append((abbrev, abbrev,))
    return choices

def get_us_state_choices(include_blank=True):
    choices = [('', '--')] if include_blank else []
    for state in US_STATES:
        abbrev = state['abbrev']
        state_name = state['state']
        choices.append((abbrev, state_name,))
    return choices
