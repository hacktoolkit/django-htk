from htk.utils import htk_setting

def help():
    event_handlers = htk_setting('HTK_SLACK_EVENT_HANDLERS')
    commands = ['`%s`' % command for command in sorted(event_handlers.keys())]
    usage = """Usage: `htk: command args`
Available commands are: %s
""" % ', '.join(commands)
    return usage

def default():
    usage = """Usage: `htk: default`
This is not a very useful command; it simply parrots back what you said (to test whether the Slack bot is functioning)."""
    return usage

def bible():
    usage = """Usage: `htk: bible [esv|nasb] passage`
    e.g.
- `htk: bible esv John 3:16`
- `htk: bible nasb 1 Cor 13:4-7`
- `htk: bible Lamentations 3:22-23`
- `htk: bible Psalm 119:11`"""
    return usage

def stock():
    usage = """Usage: `htk: stock SYMBOL [SYMBOLS]`
    e.g.
- `htk: stock AAPL AMZN GOOG LNKD YHOO`"""
    return usage

def weather():
    usage = """Usage: `htk: weather LOCATION`
e.g.
- `htk: weather 90210`
- `htk: weather San Francisco, CA`
- `htk: weather 1600 Pennsylvania Ave NW, Washington, DC 20500`"""
    return usage
