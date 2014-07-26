Stripe Lib for django-htk
=========================

Testing

https://stripe.com/docs/testing

In test mode, you can use these test cards to simulate a successful transaction:

Number                     Card type
4242 4242 4242 4242        Visa
4012 8888 8888 1881        Visa
4000 0566 5566 5556        Visa (debit)
5555 5555 5555 4444        MasterCard
5200 8282 8282 8210        MasterCard (debit)
5105 1051 0510 5100        MasterCard (prepaid)
3782 822463 10005          American Express
3714 496353 98431          American Express
6011 1111 1111 1117        Discover
6011 0009 9013 9424        Discover
3056 9309 0259 04          Diners Club
3852 0000 0232 37          Diners Club
3530 1113 3330 0000        JCB
3566 0020 2036 0505        JCB

In addition, these cards will produce specific responses that are useful for testing different scenarios:

Number                     Description
4000 0000 0000 0010        With default account settings, charge will succeed but address_line1_check and address_zip_check will both fail.
4000 0000 0000 0028        With default account settings, charge will succeed but address_line1_check will fail.
4000 0000 0000 0036        With default account settings, charge will succeed but address_zip_check will fail.
4000 0000 0000 0044        With default account settings, charge will succeed but address_zip_check and address_line1_check will both be unchecked.
4000 0000 0000 0101        With default account settings, charge will succeed but cvc_check will fail if a CVC is entered.
4000 0000 0000 0341        Attaching this card to a Customer object will succeed, but attempts to charge the customer will fail.
4000 0000 0000 0002        Charges with this card will always be declined with a card_declined code.
4000 0000 0000 0127        Charge will be declined with an incorrect_cvc code.
4000 0000 0000 0069        Charge will be declined with an expired_card code.
4000 0000 0000 0119        Charge will be declined with a processing_error code.

Additional test mode validation: By default, passing address or CVC data with the card number will cause the address and CVC checks to succeed. If not specified, the value of the checks will be null. Any expiration date in the future will be considered valid.

How do I test specific error codes?

Some suggestions:

card_declined: Use this special card number - 4000000000000002.
incorrect_number: Use a number that fails the Luhn check, e.g. 4242424242424241.
invalid_expiry_month: Use an invalid month e.g. 13.
invalid_expiry_year: Use a year in the past e.g. 1970.
invalid_cvc: Use a two digit number e.g. 99.
