def digits_of(n):
    digits = [int(d) for d in str(n)]
    return digits

#####
# http://en.wikipedia.org/wiki/Luhn_algorithm


def luhn_checksum(card_number):
    """Calculates the Luhn checksum of the digits in `card_number`, modulo 10
    """
    def _double_and_sum_digits(d):
        s = d * 2
        result = s if s < 10 else (s - 9)
        return result

    mapped_digits = [
        d if index % 2 == 0 else _double_and_sum_digits(d)
        for index, d
        in enumerate(reversed(digits_of(card_number)))
    ]

    checksum = sum(mapped_digits) % 10
    return checksum


def is_luhn_valid(card_number):
    """Determines whether `card_number` is valid according to the Luhn algorithm
    """
    is_valid = luhn_checksum(card_number) == 0
    return is_valid


def calculate_luhn_check_digit(partial_card_number):
    """Calculates the check digit for a partial number using the Luhn algorithm
    """
    checksum = luhn_checksum(int(partial_card_number) * 10)
    if checksum == 0:
        check_digit = 0
    else:
        check_digit = 10 - checksum
    return check_digit


def calculate_luhn(partial_card_number):
    return calculate_luhn_check_digit(partial_card_number)
