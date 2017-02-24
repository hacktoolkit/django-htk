import re

from htk.lib.slack.utils import get_event_handler_usages
from htk.lib.slack.utils import is_available_command
from htk.lib.slack.utils import parse_event_text
from htk.lib.slack.utils import webhook_call

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
    event_handler_usages = get_event_handler_usages(event)
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

    payload = {
        'text' : slack_text,
    }
    return payload

@preprocess_event
def bart(event, **kwargs):
    """BART event handler for Slack webhook events
    """
    text = kwargs.get('text')
    command = kwargs.get('command')
    args = kwargs.get('args')

    if command == 'bart':
        if args:
            arg_parts = args.split()
            arg1 = arg_parts[0].lower()
            if arg1 == 'stations':
                from htk.lib.sfbart.utils import get_bart_stations
                stations = get_bart_stations()
                slack_text = 'BART stations:\n%s' % '\n'.join(['%s (%s)' % (station['name'], station['abbrev'],) for station in stations])
            elif len(arg_parts) == 2:
                # two stations, assume departure lookup
                from htk.lib.sfbart.utils import get_bart_schedule_depart
                orig_station = arg_parts[0].lower()
                dest_station = arg_parts[1].lower()
                data = get_bart_schedule_depart(orig_station, dest_station)
                data['formatted_trips'] = '\n'.join([
                    '%(origTimeMin)s - %(destTimeMin)s (%(tripTime)s mins)' % trip
                    for trip
                    in data['trips']
                ])
                slack_text = """*%(orig_station_name)s* (%(origin)s) to *%(dest_station_name)s* (%(destination)s)
%(formatted_trips)s
""" % data
            else:
                slack_text = 'No handler for specified arguments.\n%s' % get_usage(event, command)
        else:
            slack_text = 'Please specify a BART request.\n%s' % get_usage(event, command)
    else:
        slack_text = 'Illegal command.'

    payload = {
        'text' : slack_text,
    }
    return payload

@preprocess_event
def beacon(event, **kwargs):
    """Beacon geo-ip location handler for Slack webhook events

    Creates a homing beacon URL for the user good for 5 minutes
    When the beacon URL is clicked, the IP address will be geo-located and shared to Slack
    """
    text = kwargs.get('text')
    command = kwargs.get('command')
    args = kwargs.get('args')

    if command == 'beacon':
        from htk.lib.slack.beacon.utils import create_slack_beacon_url
        beacon_url = create_slack_beacon_url(event)
        if beacon_url:
            beacon_text = 'Open this URL to trigger the beacon: %s' % beacon_url
            user_channel = '@%s' % event['user_name']
            webhook_url = event['webhook_settings']['slack_webhook_url']
            webhook_call(
                webhook_url=webhook_url,
                text=beacon_text,
                channel=user_channel,
                unfurl_links=False,
                unfurl_media=False,
            )
            slack_text = 'Homing beacon message deployed to <%s>.' % user_channel
        else:
            slack_text = 'Slack homing beacon not set up correctly.'
    else:
        slack_text = 'Illegal command.'

    payload = {
        'text' : slack_text,
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

    payload = {
        'text' : slack_text,
    }
    return payload

@preprocess_event
def emaildig(event, **kwargs):
    """Email dig event handler for Slack webhook events
    """
    text = kwargs.get('text')
    command = kwargs.get('command')
    args = kwargs.get('args')

    if command == 'emaildig':
        if args:
            parts = re.sub(r'\<.*\|(.*)\>', r'\g<1>', args).split(' ')
            if len(parts) > 1:
                slack_text= 'Too many arguments. See usage. `%s`' % args
            else:
                email = parts[0]
                from htk.utils import htk_setting
                from htk.utils import resolve_method_dynamically
                find_person_by_email = resolve_method_dynamically(htk_setting('HTK_EMAIL_PERSON_RESOLVER'))
                person = find_person_by_email(email)
                if person:
                    slack_text = 'The following information was retrieved for *%s*:\n%s' % (email, person.as_slack())
                else:
                    slack_text = 'No information was found for email: %s' % email
        else:
            slack_text = 'Missing arguments. See usage.'
    else:
        slack_text = 'Illegal command.'

    channel = event['channel_id']

    payload = {
        'text' : slack_text,
    }
    return payload

@preprocess_event
def findemail(event, **kwargs):
    """Find email event handler for Slack webhook events
    """
    text = kwargs.get('text')
    command = kwargs.get('command')
    args = kwargs.get('args')

    if command == 'findemail':
        if args:
            parts = re.sub(r'\<.*\|(.*)\>', r'\g<1>', args).rsplit('|', 3)
            domain, first_name, middle_name, last_name = parts

            from htk.utils.emails import find_company_emails_for_name
            emails = find_company_emails_for_name(
                domain,
                first_name=first_name,
                middle_name=middle_name,
                last_name=last_name
            )
            if emails:
                slack_text = 'Found emails:\n%s' % ', '.join(emails)
            else:
                slack_text = 'No emails were found'
        else:
            slack_text = 'Missing arguments. See usage.'
    else:
        slack_text = 'Illegal command.'

    channel = event['channel_id']

    payload = {
        'text' : slack_text,
    }
    return payload

@preprocess_event
def geoip(event, **kwargs):
    """GeoIP event handler for Slack webhook events
    """
    text = kwargs.get('text')
    command = kwargs.get('command')
    args = kwargs.get('args')

    if command == 'geoip':
        if args:
            ip = args
            from htk.lib.slack.messages import slack_message_geoip
            slack_text = slack_message_geoip(ip)
        else:
            slack_text = 'Please specify an IP address.'
    else:
        slack_text = 'Illegal command.'

    channel = event['channel_id']

    payload = {
        'text' : slack_text,
        'unfurl_links' : True,
        'unfurl_media' : True,
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

    payload = {
        'text' : slack_text,
    }
    return payload

@preprocess_event
def utcnow_slack(event, **kwargs):
    """utcnow event handler for Slack webhook events
    """
    text = kwargs.get('text')
    command = kwargs.get('command')
    args = kwargs.get('args')

    if command == 'utcnow':
        from htk.utils import utcnow
        now = utcnow()
        webhook_settings = event['webhook_settings']
        user_id = webhook_settings['user']
        from htk.apps.accounts.utils import get_user_by_id
        user = get_user_by_id(user_id)
        slack_text = """*The time is now*:\n
*UTC*: %s
*%s*: %s""" % (
    now,
    user.profile.get_timezone(),
    user.profile.get_local_time(dt=now),
)
    else:
        slack_text = 'Illegal command.'

    payload = {
        'text' : slack_text,
    }
    return payload

@preprocess_event
def weather(event, **kwargs):
    """Weather event handler for Slack webhook events
    """
    text = kwargs.get('text')
    command = kwargs.get('command')
    args = kwargs.get('args')
    icon_emoji = None

    if command == 'weather':
        if args:
            location = args
            from htk.lib.darksky.utils import generate_weather_report
            from htk.utils.text.converters import markdown2slack
            from htk.utils.weather import get_weather
            weather = get_weather(location)
            formatted_weather = generate_weather_report(weather, extended=True)
            slack_text = '*Weather for %s*:\n%s' % (
                location,
                markdown2slack(formatted_weather['summary']),
            )
            icon_emoji = formatted_weather.get('icon_emoji')
        else:
            slack_text = 'Please specify a location to retrieve weather for.'
    else:
        slack_text = 'Illegal command.'

    channel = event['channel_id']

    payload = {
        'text' : slack_text,
        'icon_emoji' : icon_emoji,
    }
    return payload

@preprocess_event
def zesty(event, **kwargs):
    """Zesty event handler for Slack webhook events
    """
    text = kwargs.get('text')
    command = kwargs.get('command')
    args = kwargs.get('args')

    zesty_slack_payload = {}
    if command == 'zesty':
        webhook_settings = event['webhook_settings']
        user_id = webhook_settings['user']
        from htk.apps.accounts.utils import get_user_by_id
        user = get_user_by_id(user_id)
        zesty_id = user.profile.get_attribute('zesty_id')
        if args:
            slack_text = '`zesty` does not take any arguments'
        elif zesty_id is None:
            slack_text = 'Error: Your account does not have a Zesty account id configured. Please check with your Slack admin.'
        else:
            from htk.lib.zesty.utils import get_zesty_lunch_menu
            dt = user.profile.get_local_time()
            slack_text = ''
            zesty_slack_payload = get_zesty_lunch_menu(zesty_id, dt)
    else:
        slack_text = 'Illegal command.'

    channel = event['channel_id']

    payload = {
        'text' : slack_text,
        'unfurl_links' : True,
        'unfurl_media' : True,
    }
    payload.update(zesty_slack_payload)
    return payload
