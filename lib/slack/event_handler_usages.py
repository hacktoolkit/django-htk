from htk.lib.slack.utils import get_event_handlers

def help(**kwargs):
    event = kwargs.get('event')
    event_handlers = get_event_handlers(event)
    commands = ['`%s`' % command for command in sorted(event_handlers.keys())]
    usage_dict = {
        'description': 'Displays available commands. Available commands are: %s' % ', '.join(commands),
        'basic' : 'htk: command args',
        'examples' : [
            'htk: help help',
        ]
    }
    return usage_dict

def default(**kwargs):
    usage_dict = {
        'description' : 'This is not a very useful command; it simply parrots back what you said (to test whether the Slack bot is functioning)',
        'basic' : 'htk: default',
        'examples' : [],
    }
    return usage_dict

def bart(**kwargs):
    usage_dict = {
        'description' : 'Gets BART information',
        'basic' : 'htk: bart',
        'examples' : [
            'htk: bart stations',
            'htk: bart <origin> <destination>',
        ],
    }
    return usage_dict

def beacon(**kwargs):
    usage_dict = {
        'description' : 'Creates a homing beacon URL for the user good for 5 minutes. When the beacon URL is clicked, the IP address will be geo-located and shared to Slack.',
        'basic' : 'htk: beacon',
        'examples' : [
        ],
    }
    return usage_dict

def bible(**kwargs):
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

def emaildig(**kwargs):
    usage_dict = {
        'description' : 'Find information about a person by email address',
        'basic' : 'htk: emaildig email',
        'examples' : [
            'htk: emaildig hello@hacktoolkit.com',
        ],
    }
    return usage_dict

def findemail(**kwargs):
    usage_dict = {
        'description' : 'Find Company-Based Email Address automagically',
        'basic' : 'htk: findemail domain|firstname|middlename|lastname',
        'examples' : [
            'htk: findemail facebook.com|mark||zuckerberg',
        ],
    }
    return usage_dict

def geoip(**kwargs):
    usage_dict = {
        'description' : 'Look up geo information for an IP address. Uses GeoIP database',
        'basic' : 'htk: geoip ip',
        'examples' : [
            'htk: geoip 8.8.8.8',
        ],
    }
    return usage_dict

def ohmygreen(**kwargs):
    usage_dict = {
        'description' : 'Look up OhMyGreen menu',
        'basic' : 'htk: ohmygreen',
        'examples' : [
            'htk: ohmygreen',
        ],
    }
    return usage_dict

def stock(**kwargs):
    usage_dict = {
        'description' : 'Look up most recent stock quotes',
        'basic': 'htk: stock SYMBOL[( |;|,)SYMBOLS]',
        'examples' : [
            'htk: stock AAPL AMZN GOOG LNKD YHOO',
        ],
    }
    return usage_dict

def utcnow_slack(**kwargs):
    usage_dict = {
        'description' : 'Get the current UTC time and some more.',
        'basic': 'htk: utcnow',
        'examples' : [
        ],
    }
    return usage_dict

def weather(**kwargs):
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

def zesty(**kwargs):
    usage_dict = {
        'description' : 'Look up Zesty lunch menu',
        'basic' : 'htk: zesty',
        'examples' : [
            'htk: zesty',
        ],
    }
    return usage_dict
