HTK_SLACK_EVENT_TYPE_RESOLVER = 'htk.lib.slack.event_resolvers.default_event_type_resolver'

HTK_SLACK_EVENT_HANDLERS = {
    'default' : 'htk.lib.slack.event_handlers.default',
    'bart' : 'htk.lib.slack.event_handlers.bart',
    'beacon' : 'htk.lib.slack.event_handlers.beacon',
    'bible' : 'htk.lib.slack.event_handlers.bible',
    'emaildig' : 'htk.lib.slack.event_handlers.emaildig',
    'findemail' : 'htk.lib.slack.event_handlers.findemail',
    'geoip' : 'htk.lib.slack.event_handlers.geoip',
    'help' : 'htk.lib.slack.event_handlers.help',
    'stock' : 'htk.lib.slack.event_handlers.stock',
    'utcnow' : 'htk.lib.slack.event_handlers.utcnow_slack',
    'weather' : 'htk.lib.slack.event_handlers.weather',
    'zesty' : 'htk.lib.slack.event_handlers.zesty',
}

HTK_SLACK_EVENT_HANDLERS_EXTRAS = {}

HTK_SLACK_EVENT_HANDLER_USAGES = {
    'help' : 'htk.lib.slack.event_handler_usages.help',
    'default' : 'htk.lib.slack.event_handler_usages.default',
    'bart' : 'htk.lib.slack.event_handler_usages.bart',
    'beacon' : 'htk.lib.slack.event_handler_usages.beacon',
    'bible' : 'htk.lib.slack.event_handler_usages.bible',
    'emaildig' : 'htk.lib.slack.event_handler_usages.emaildig',
    'findemail' : 'htk.lib.slack.event_handler_usages.findemail',
    'geoip' : 'htk.lib.slack.event_handler_usages.geoip',
    'stock' : 'htk.lib.slack.event_handler_usages.stock',
    'utcnow' : 'htk.lib.slack.event_handler_usages.utcnow_slack',
    'weather' : 'htk.lib.slack.event_handler_usages.weather',
    'zesty' : 'htk.lib.slack.event_handler_usages.zesty',
}

HTK_SLACK_EVENT_HANDLER_USAGES_EXTRA = {}

# trigger words that are also commands
HTK_SLACK_TRIGGER_COMMAND_WORDS = (
    'bible',
    'findemail',
    'stock',
    'weather',
)

# notifications
HTK_SLACK_NOTIFICATIONS_ENABLED = False

# channels
HTK_SLACK_DEBUG_CHANNEL = '#test'
HTK_SLACK_NOTIFICATIONS_CHANNEL = '#test'

# url names (routes)
HTK_SLACK_BEACON_URL_NAME = None
