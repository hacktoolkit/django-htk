# HTK Imports
from htk.constants.geo import (
    US_STATE_CODES_LOOKUP,
    US_STATES,
    US_STATES_LOOKUP,
)


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


def get_us_state_code_by_name(state_name):
    state_code = US_STATE_CODES_LOOKUP.get(state_name)
    return state_code


def get_us_state_code(state):
    """Get a US state code for `state`, which is either a state code or state name
    """
    if state in US_STATES_LOOKUP:
        state_code = state
    else:
        state_code = get_us_state_code_by_name(state)
    return state_code
