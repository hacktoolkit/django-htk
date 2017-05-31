def preprocess_event(event_handler):
    def wrapped_event_handler(event):
        kwargs = {
            'intent' : event['request']['intent'],
        }
        payload = event_handler(event, **kwargs)
        return payload
    return wrapped_event_handler

@preprocess_event
def default(event, **kwargs):
    """A Hacktoolkit-flavored default event handler for Alexa webhook events

    Returns a payload if applicable, or None
    """
    intent = kwargs.get('intent')

    payload = {
        'version' : '1.0',
        'response' : {
            'outputSpeech' : {
                'type' : 'SSML',
                'ssml' : """<speak>Sorry, I'm not sure how to process that.</speak>""",
            }
        },
    }
    return payload

@preprocess_event
def zesty(event, **kwargs):
    """Zesty event handler for Alexa skill webhook events

    https://developer.amazon.com/public/solutions/alexa/alexa-skills-kit/docs/speech-synthesis-markup-language-ssml-reference
    """
    intent = kwargs.get('intent')

    if intent['name'] == 'ZestyLunchIntent':
        #webhook_settings = event['webhook_settings']
        #user_id = webhook_settings['user']
        #from htk.apps.accounts.utils import get_user_by_id
        #user = get_user_by_id(user_id)
        # TODO: hardcoded
        from htk.apps.accounts.utils import get_user_by_username
        user = get_user_by_username('hacktoolkit')
        zesty_id = user.profile.get_attribute('zesty_id')
        if zesty_id is None:
            ssml = """<speak>Your account does not have a Zesty account id configured. Please check with your Alexa skills admin.</speak>"""
        else:
            from htk.lib.zesty.utils import get_zesty_lunch_menu_ssml
            dt = user.profile.get_local_time()
            ssml = get_zesty_lunch_menu_ssml(zesty_id, dt)
    else:
        ssml = """<speak>Sorry, I'm having difficulties processing that.</speak>"""

    payload = {
        'version' : '1.0',
        'response' : {
            'outputSpeech' : {
                'type' : 'SSML',
                'ssml' : ssml,
            },
        },
    }
    return payload
