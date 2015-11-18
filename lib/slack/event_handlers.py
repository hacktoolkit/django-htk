import re

from htk.lib.slack.utils import parse_event_text
from htk.utils import htk_setting

def help(event):
    (text, command, args,) = parse_event_text(event)
    event_handlers = htk_setting('HTK_SLACK_EVENT_HANDLERS')

    if command == 'help':
        commands = ['`%s`' % command for command in sorted(event_handlers.keys())]
        slack_text = """Usage: `htk: command args`
Available commands are: %s
""" % ', '.join(commands)
    else:
        slack_text = 'Illegal command.'

    username = 'Hacktoolkit Bot'
    payload = {
        'text' : slack_text,
        'username' : username,
    }
    return payload


def default(event):
    """A Hacktoolkit-flavored default event handler for Slack webhook events

    Returns a payload if applicable, or None
    """
    (text, command, args,) = parse_event_text(event)

    # for example, we could...
    # make another webhook call in response
    channel = event['channel_id']
    echo_text = 'You said: [%s]. Roger that.' % text
    username = 'Hacktoolkit Bot'
    #webhook_call(text=echo_text, channel=channel, username=username)

    payload = {
        'text' : echo_text,
        'username' : username,
    }
    return payload

def bible(event):
    """Bible event handler for Slack webhook events
    """
    (text, command, args,) = parse_event_text(event)

    if command == 'bible':
        if args:
            location = args
            from htk.lib.literalword.utils import get_bible_passage
            #from htk.utils.text.converters import markdown2slack
            webhook_settings = event.get('webhook_settings', {})
            bible_version = webhook_settings.get('bible_version', None)
            passage = get_bible_passage(args, version=bible_version)
            passage['query'] = args
            slack_text = """Bible passage: *%(query)s*
Read on Literal Word: %(url)s
>>> %(text)s
""" % passage
        else:
            slack_text = 'Please specify a Bible passage to look up. e.g. `htk: bible Lamentations 3:22-23` or `htk: bible Psalm 119:11`'
    else:
        slack_text = 'Illegal command.'

    username = 'Hacktoolkit Bot'

    payload = {
        'text' : slack_text,
        'username' : username,
    }
    return payload

def stock(event):
    """Stock event handler for Slack webhook events
    """
    (text, command, args,) = parse_event_text(event)

    if command == 'stock':
        if args:
            STOCK_TICKER_MAX_LENGTH = 5
            symbols = map(lambda x: x.upper(), filter(lambda x: 0 < len(x) <= STOCK_TICKER_MAX_LENGTH, re.split(r'[;, ]', args)))
            # remove duplicates
            symbols = list(set(symbols))
            # cap number of symbols per request
            MAX_SYMBOLS = 20
            symbols = symbols[:MAX_SYMBOLS]
            from htk.lib.yahoo.finance.utils import get_stock_price
            prices = {}
            for symbol in symbols:
                prices[symbol] = get_stock_price(symbol)
            prices_strings = ['*%s* - $%s' % (symbol, prices[symbol],) for symbol in sorted(prices.keys())]
            slack_text = '\n'.join(prices_strings)
        else:
            slack_text = 'Please enter a list of stock symbols to look up.'
    else:
        slack_text = 'Illegal command.'

    username = 'Hacktoolkit Bot'
    payload = {
        'text' : slack_text,
        'username' : username,
    }
    return payload

def weather(event):
    """Weather event handler for Slack webhook events
    """
    (text, command, args,) = parse_event_text(event)

    if command == 'weather':
        if args:
            location = args
            from htk.lib.forecastio.utils import format_weather
            from htk.utils.text.converters import markdown2slack
            from htk.utils.weather import get_weather
            weather = get_weather(location)
            formatted_weather = format_weather(weather)
            slack_text = '*Weather for %s*:\n%s' % (
                location,
                markdown2slack(formatted_weather),
            )
        else:
            slack_text = 'Please specify a location to retrieve weather for.'
    else:
        slack_text = 'Illegal command.'

    channel = event['channel_id']
    username = 'Hacktoolkit Bot'

    payload = {
        'text' : slack_text,
        'username' : username,
    }
    return payload
