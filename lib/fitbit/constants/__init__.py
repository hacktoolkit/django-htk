FITBIT_API_BASE_URL = 'https://api.fitbit.com'

FITBIT_API_RESOURCES = {
    # permissions
    'refresh': '/oauth2/token',
    'revoke': '/oauth2/revoke',
    # activity
    'activity-steps-monthly': '/1/user/-/activities/steps/date/today/1m.json',
    # body & weight
    'fat': lambda date: '/1/user/-/body/log/fat/date/{}.json'.format(date),
    'weight': lambda date: '/1/user/-/body/log/weight/date/{}.json'.format(
        date
    ),
    # settings
    'devices': '/1/user/-/devices.json',
}
