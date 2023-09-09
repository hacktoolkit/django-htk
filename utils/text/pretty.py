def phonenumber(value, country='US'):
    """Formats a phone number for a country
    """
    import phonenumbers
    try:
        formatted = phonenumbers.format_number(phonenumbers.parse(value, country), phonenumbers.PhoneNumberFormat.NATIONAL)
    except:
        formatted = value
    return formatted
