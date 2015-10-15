from htk.lib.slack.utils import parse_event_text

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
            passage = get_bible_passage(args)
            passage['query'] = args
            slack_text = """Bible passage: *%(query)s*
Read on LiteralWord: %(url)s
>>> %(text)s
""" % passage
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
