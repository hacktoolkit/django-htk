ITERABLE_API_BASE_URL = 'https://api.iterable.com/api'

ITERABLE_API_RESOURCES = {
    ##
    # events
    'event_track' : '/events/track',
    ##
    # users
    'user_delete' : '/users/%(email)s',
    ##
    # workflows
    'workflow_trigger' : '/workflows/triggerWorkflow',
}

ITERABLE_DATE_FORMAT = '%Y-%m-%d %H:%M:%S %z'
