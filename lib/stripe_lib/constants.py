STRIPE_ID_PREFIX_CARD = 'card_'
STRIPE_ID_PREFIX_CHARGE = 'ch_'
STRIPE_ID_PREFIX_CUSTOMER = 'cus_'
STRIPE_ID_PREFIX_RECIPIENT = 'rp_'
STRIPE_ID_PREFIX_TOKEN = 'tok_'

STRIPE_TEST_CARDS = {
    'visa' : [
        {
            'number' : '4242424242424242',
        },
        {
            'number' : '4012888888881881',
        },
    ],
    'visa_debit' : [
        {
            'number' : '4000056655665556',
        },
    ],
    'mc' : [
        {
            'number' : '5555555555554444',
        },
    ],
    'mc_debit' : [
        {
            'number' : '5200828282828210',
        },
    ],
    'mc_prepaid' : [
        {
            'number' : '5105105105105100',
        },
    ],
    'amex' : [
        {
            'number' : '378282246310005',
        },
        {
            'number' : '371449635398431',
        },
    ],
    'discover' : [
        {
            'number' : '6011111111111117',
        },
        {
            'number' : '6011000990139424',
        },
    ],
    'diners' : [
        {
            'number' : '30569309025904',
        },
        {
            'number' : '38520000023237',
        },
    ],
    'jcb' : [
        {
            'number' : '353011133330000',
        },
        {
            'number' : '3566002020360505',
        },
    ]
}
