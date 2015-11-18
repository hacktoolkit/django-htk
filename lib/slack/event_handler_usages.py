from htk.utils import htk_setting

def help():
    event_handlers = htk_setting('HTK_SLACK_EVENT_HANDLERS')
    commands = ['`%s`' % command for command in sorted(event_handlers.keys())]
    usage_dict = {
        'description': 'Displays available commands. Available commands are: %s' % ', '.join(commands),
        'basic' : 'htk: command args',
        'examples' : [
            'htk: help help',
        ]
    }
    return usage_dict

def default():
    usage_dict = {
        'description' : 'This is not a very useful command; it simply parrots back what you said (to test whether the Slack bot is functioning)',
        'basic' : 'htk: default',
        'examples' : [],
    }
    return usage_dict

def bible():
    usage_dict = {
        'description' : 'Look up a Bible passage',
        'basic' : 'htk: bible [esv|nasb] passage',
        'examples' : [
            'htk: bible esv John 3:16',
            'htk: bible nasb 1 Cor 13:4-7',
            'htk: bible Lamentations 3:22-23',
            'htk: bible Psalm 119:11',
        ],
    }
    return usage_dict

def stock():
    usage_dict = {
        'description' : 'Look up most recent stock quotes',
        'basic': 'htk: stock SYMBOL[( |;|,)SYMBOLS]',
        'examples' : [
            'htk: stock AAPL AMZN GOOG LNKD YHOO',
        ],
    }
    return usage_dict

def weather():
    usage_dict = {
        'description' : 'Look up weather',
        'basic' : 'htk: weather LOCATION',
        'examples' : [
            'htk: weather 90210',
            'htk: weather San Francisco, CA',
            'htk: weather 1600 Pennsylvania Ave NW, Washington, DC 20500',
        ],
    }
    return usage_dict
