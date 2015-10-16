PLIVO_MESSAGE_WEBHOOK_PARAMS = (
    'From', # 14085551212
    'TotalRate',
    'Text',
    'To', # 14151234567
    'Units',
    'TotalAmount',
    'Type', # sms
    'MessageUUID',
)

PLIVO_SLACK_DEFAULT_MESSAGE_FORMAT = u'Plivo Message from *%(From)s* (%(Type)s; %(MessageUUID)s)\n>>> %(Text)s'
