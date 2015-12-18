from htk.utils import htk_setting

def slack_debug(message):
    from htk.lib.slack.utils import webhook_call
    channel = htk_setting('HTK_SLACK_DEBUG_CHANNEL')
    webhook_call(text=message, channel=channel)
