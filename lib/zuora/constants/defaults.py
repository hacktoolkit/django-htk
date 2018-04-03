HTK_ZUORA_USERNAME = None
HTK_ZUORA_PASSWORD = None
HTK_ZUORA_COUNTRY = 'US' # 'US' or 'EU'
HTK_ZUORA_PROD = False

HTK_ZUORA_HANDLE_UNHANDLED_EVENTS = False

HTK_ZUORA_EVENT_TYPES = {
    'default' : 'Default (unhandled) event',
    # billing
    # payments
    'subscription_created' : 'Subscription created',
    # finance
}

HTK_ZUORA_EVENT_HANDLERS = {
    'default' : 'htk.lib.zuora.event_handlers.default',
    'subscription_created' : 'htk.lib.zuora.event_handlers.subscription_created',
}
