import re

from htk.lib.slack.utils import is_available_command
from htk.lib.slack.utils import parse_event_text
from htk.utils import htk_setting

def preprocess_event(event_handler):
    def wrapped_event_handler(event):
        (text, command, args,) = parse_event_text(event)
        if args:
            arg_parts = args.split()
            arg1 = arg_parts[0].lower()
            if arg1 == 'help':
                slack_text = get_usage(event, command)
                username = 'Hacktoolkit Bot'
                payload = {
                    'text' : slack_text,
                    'username' : username,
                }
            else:
                payload = None
        else:
            payload = None
        if payload is None:
            kwargs = {
                'text' : text,
                'command' : command,
                'args' : args,
            }
            payload = event_handler(event, **kwargs)
        return payload
    return wrapped_event_handler

def get_usage(event, command):
    event_handler_usages = htk_setting('HTK_SLACK_EVENT_HANDLER_USAGES')
    from htk.utils.general import resolve_method_dynamically
    usage_fn_module_str = event_handler_usages.get(command)
    usage_fn = resolve_method_dynamically(usage_fn_module_str)
    if type(usage_fn) == type(lambda x: True):
        # <type 'function'>
        kwargs = {
            'event' : event,
        }
        usage_dict = usage_fn(**kwargs)
    else:
        usage_dict = {
            'description' : 'Not specified',
            'basic' : 'htk: %s' % command,
            'examples' : [],
        }
    if usage_dict['examples']:
        formatted_examples = '```%s```' % '\n'.join('    %s' % example for example in usage_dict['examples'])
    else:
        formatted_examples = 'N/A'
    usage_dict['formatted_examples'] = formatted_examples
    usage = """*Usage*: %(description)s
`    %(basic)s`
*Examples*:
%(formatted_examples)s""" % usage_dict
    return usage

@preprocess_event
def help(event, **kwargs):
    text = kwargs.get('text')
    command = kwargs.get('command')
    args = kwargs.get('args')

    if command == 'help':
        if args:
            arg_parts = args.split()
            arg1 = arg_parts[0].lower()
            if is_available_command(event, arg1):
                # override the command to get help for
                command = arg1
        slack_text = get_usage(event, command)
    else:
        slack_text = 'Illegal command.'

    username = 'Hacktoolkit Bot'
    payload = {
        'text' : slack_text,
        'username' : username,
    }
    return payload

@preprocess_event
def default(event, **kwargs):
    """A Hacktoolkit-flavored default event handler for Slack webhook events

    Returns a payload if applicable, or None
    """
    text = kwargs.get('text')
    command = kwargs.get('command')
    args = kwargs.get('args')

    # for example, we could...
    # make another webhook call in response
    channel = event['channel_id']
    slack_text = 'You said:\n>%s\n Roger that.' % text
    #webhook_call(text=slack_text, channel=channel, username=username)

    username = 'Hacktoolkit Bot'
    payload = {
        'text' : slack_text,
        'username' : username,
    }
    return payload

@preprocess_event
def bible(event, **kwargs):
    """Bible event handler for Slack webhook events
    """
    text = kwargs.get('text')
    command = kwargs.get('command')
    args = kwargs.get('args')

    if command == 'bible':
        if args:
            from htk.lib.literalword.utils import get_bible_passage
            from htk.lib.literalword.utils import is_bible_version
            #from htk.utils.text.converters import markdown2slack
            arg_parts = args.split()
            arg1 = arg_parts[0].lower()
            if is_bible_version(arg1):
                bible_version = arg1
                args = ' '.join(arg_parts[1:])
            else:
                webhook_settings = event.get('webhook_settings', {})
                bible_version = webhook_settings.get('bible_version', None)
            passage = get_bible_passage(args, version=bible_version)
            passage['query'] = args
            slack_text = """Bible passage: *%(query)s*
Read on Literal Word: %(url)s
>>> %(text)s
""" % passage
        else:
            slack_text = 'Please specify a Bible passage to look up.\n%s' % get_usage(event, command)
    else:
        slack_text = 'Illegal command.'

    username = 'Hacktoolkit Bot'

    payload = {
        'text' : slack_text,
        'username' : username,
    }
    return payload

@preprocess_event
def stock(event, **kwargs):
    """Stock event handler for Slack webhook events
    """
    text = kwargs.get('text')
    command = kwargs.get('command')
    args = kwargs.get('args')

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

@preprocess_event
def weather(event, **kwargs):
    """Weather event handler for Slack webhook events
    """
    text = kwargs.get('text')
    command = kwargs.get('command')
    args = kwargs.get('args')

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
