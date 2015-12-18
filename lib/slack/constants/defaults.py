HTK_SLACK_EVENT_TYPE_RESOLVER = 'htk.lib.slack.event_resolvers.default_event_type_resolver'

HTK_SLACK_EVENT_HANDLERS = {
    'default' : 'htk.lib.slack.event_handlers.default',
    'bible' : 'htk.lib.slack.event_handlers.bible',
    'help' : 'htk.lib.slack.event_handlers.help',
    'stock' : 'htk.lib.slack.event_handlers.stock',
    'weather' : 'htk.lib.slack.event_handlers.weather',
}

HTK_SLACK_EVENT_HANDLER_USAGES = {
    'help' : 'htk.lib.slack.event_handler_usages.help',
    'default' : 'htk.lib.slack.event_handler_usages.default',
    'bible' : 'htk.lib.slack.event_handler_usages.bible',
    'stock' : 'htk.lib.slack.event_handler_usages.stock',
    'weather' : 'htk.lib.slack.event_handler_usages.weather',
}

# trigger words that are also commands
HTK_SLACK_TRIGGER_COMMAND_WORDS = (
    'bible',
    'stock',
    'weather',
)

# notifications
HTK_SLACK_NOTIFICATIONS_ENABLED = False

# channels
HTK_SLACK_DEBUG_CHANNEL = '#test'
HTK_SLACK_NOTIFICATIONS_CHANNEL = '#test'
