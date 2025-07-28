HTK_SLACK_EVENT_TYPE_RESOLVER = 'htk.lib.slack.event_resolvers.default_event_type_resolver'

HTK_SLACK_EVENT_HANDLERS = {
    'default' : 'htk.lib.slack.event_handlers.default',
    'bart' : 'htk.lib.slack.event_handlers.bart',
    'beacon' : 'htk.lib.slack.event_handlers.beacon',
    'bible' : 'htk.lib.slack.event_handlers.bible',
    'emaildig' : 'htk.lib.slack.event_handlers.emaildig',
    'findemail' : 'htk.lib.slack.event_handlers.findemail',
    'geoip' : 'htk.lib.slack.event_handlers.geoip',
    'githubprs': 'htk.lib.slack.event_handlers.github_prs',
    'help' : 'htk.lib.slack.event_handlers.help',
    'ohmygreen' : 'htk.lib.slack.event_handlers.ohmygreen',
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
    'githubprs': 'htk.lib.slack.event_handler_usages.github_prs',
    'ohmygreen' : 'htk.lib.slack.event_handler_usages.ohmygreen',
    'stock' : 'htk.lib.slack.event_handler_usages.stock',
    'utcnow' : 'htk.lib.slack.event_handler_usages.utcnow_slack',
    'weather' : 'htk.lib.slack.event_handler_usages.weather',
    'zesty' : 'htk.lib.slack.event_handler_usages.zesty',
}

HTK_SLACK_EVENT_HANDLER_USAGES_EXTRA = {}


# trigger words that are also commands
HTK_SLACK_TRIGGER_COMMAND_WORDS = (
    'bart',
    'bible',
    'findemail',
    'stock',
    'weather',
)


##
# Notifications
HTK_SLACK_NOTIFICATIONS_ENABLED = False
HTK_SLACK_BOT_ENABLED = False


##
# Channels
HTK_SLACK_NOTIFICATION_CHANNELS = {
    'critical' : '#alerts-p0-critical',
    'severe'   : '#alerts-p1-severe',
    'danger'   : '#alerts-p2-danger',
    'warning'  : '#alerts-p3-warning',
    'info'     : '#alerts-p4-info',
    'debug'    : '#alerts-p5-debug',
}
HTK_SLACK_DEBUG_CHANNEL = '#test'
HTK_SLACK_CELERY_NOTIFICATIONS_CHANNEL = None

HTK_SLACK_PRODUCTION_ERROR_CHANNEL_LEVEL = 'danger'

##
# url names (routes)
HTK_SLACK_BEACON_URL_NAME = None


##
# Celery Tasks

HTK_SLACK_CELERY_TASK_GITHUB_PRS = None
