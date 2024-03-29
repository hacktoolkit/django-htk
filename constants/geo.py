US_STATES = [
    {
        'state': 'Alabama',
        'abbrev': 'AL',
    },
    {
        'state': 'Alaska',
        'abbrev': 'AK',
    },
    {
        'state': 'Arizona',
        'abbrev': 'AZ',
    },
    {
        'state': 'Arkansas',
        'abbrev': 'AR',
    },
    {
        'state': 'California',
        'abbrev': 'CA',
    },
    {
        'state': 'Colorado',
        'abbrev': 'CO',
    },
    {
        'state': 'Connecticut',
        'abbrev': 'CT',
    },
    {
        'state': 'Delaware',
        'abbrev': 'DE',
    },
    {
        'state': 'Florida',
        'abbrev': 'FL',
    },
    {
        'state': 'Georgia',
        'abbrev': 'GA',
    },
    {
        'state': 'Hawaii',
        'abbrev': 'HI',
    },
    {
        'state': 'Idaho',
        'abbrev': 'ID',
    },
    {
        'state': 'Illinois',
        'abbrev': 'IL',
    },
    {
        'state': 'Indiana',
        'abbrev': 'IN',
    },
    {
        'state': 'Iowa',
        'abbrev': 'IA',
    },
    {
        'state': 'Kansas',
        'abbrev': 'KS',
    },
    {
        'state': 'Kentucky',
        'abbrev': 'KY',
    },
    {
        'state': 'Louisiana',
        'abbrev': 'LA',
    },
    {
        'state': 'Maine',
        'abbrev': 'ME',
    },
    {
        'state': 'Maryland',
        'abbrev': 'MD',
    },
    {
        'state': 'Massachusetts',
        'abbrev': 'MA',
    },
    {
        'state': 'Michigan',
        'abbrev': 'MI',
    },
    {
        'state': 'Minnesota',
        'abbrev': 'MN',
    },
    {
        'state': 'Mississippi',
        'abbrev': 'MS',
    },
    {
        'state': 'Missouri',
        'abbrev': 'MO',
    },
    {
        'state': 'Montana',
        'abbrev': 'MT',
    },
    {
        'state': 'Nebraska',
        'abbrev': 'NE',
    },
    {
        'state': 'Nevada',
        'abbrev': 'NV',
    },
    {
        'state': 'New Hampshire',
        'abbrev': 'NH',
    },
    {
        'state': 'New Jersey',
        'abbrev': 'NJ',
    },
    {
        'state': 'New Mexico',
        'abbrev': 'NM',
    },
    {
        'state': 'New York',
        'abbrev': 'NY',
    },
    {
        'state': 'North Carolina',
        'abbrev': 'NC',
    },
    {
        'state': 'North Dakota',
        'abbrev': 'ND',
    },
    {
        'state': 'Ohio',
        'abbrev': 'OH',
    },
    {
        'state': 'Oklahoma',
        'abbrev': 'OK',
    },
    {
        'state': 'Oregon',
        'abbrev': 'OR',
    },
    {
        'state': 'Pennsylvania',
        'abbrev': 'PA',
    },
    {
        'state': 'Rhode Island',
        'abbrev': 'RI',
    },
    {
        'state': 'South Carolina',
        'abbrev': 'SC',
    },
    {
        'state': 'South Dakota',
        'abbrev': 'SD',
    },
    {
        'state': 'Tennessee',
        'abbrev': 'TN',
    },
    {
        'state': 'Texas',
        'abbrev': 'TX',
    },
    {
        'state': 'Utah',
        'abbrev': 'UT',
    },
    {
        'state': 'Vermont',
        'abbrev': 'VT',
    },
    {
        'state': 'Virginia',
        'abbrev': 'VA',
    },
    {
        'state': 'Washington',
        'abbrev': 'WA',
    },
    {
        'state': 'West Virginia',
        'abbrev': 'WV',
    },
    {
        'state': 'Wisconsin',
        'abbrev': 'WI',
    },
    {
        'state': 'Wyoming',
        'abbrev': 'WY',
    },
]


US_FEDERAL_DISTRICTS = [
    # https://en.wikipedia.org/wiki/Washington,_D.C.
    {
        'state': 'District of Columbia',
        'abbrev': 'DC',
    },
]


# https://en.wikipedia.org/wiki/Territories_of_the_United_States
US_TERRITORIES = [
    {
        'state': 'American Samoa',
        'abbrev': 'AS',
    },
    {
        'state': 'Guam',
        'abbrev': 'GU',
    },
    {
        'state': 'Northern Mariana Islands',
        'abbrev': 'MP',
    },
    {
        'state': 'Puerto Rico',
        'abbrev': 'PR',
    },
    {
        'state': 'United Stated Virgin Islands',
        'abbrev': 'VI',
    },
]


ALL_US_STATES_AND_TERRITORIES = (
    US_STATES
    + US_FEDERAL_DISTRICTS
    + US_TERRITORIES
)


US_STATE_CODES_LOOKUP = {
    state['state']: state['abbrev']
    for state
    in ALL_US_STATES_AND_TERRITORIES
}


US_STATES_LOOKUP = {
    state_code: state_name
    for state_name, state_code
    in US_STATE_CODES_LOOKUP.items()
}


ALL_US_STATES_AND_TERRITORIES_ORDERED_BY_NAME = sorted(
    ALL_US_STATES_AND_TERRITORIES,
    key=lambda state: state['state']
)


ALL_US_STATES_AND_TERRITORIES_ORDERED_BY_STATE_CODE = sorted(
    ALL_US_STATES_AND_TERRITORIES,
    key=lambda state: state['abbrev']
)
