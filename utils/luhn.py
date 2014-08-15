def digits_of(n):
    digits = [int(d) for d in str(n)]
    return digits

#####
# http://en.wikipedia.org/wiki/Luhn_algorithm

def luhn_checksum(card_number):
    digits = digits_of(card_number)
    odd_digits = digits[-1::-2]
    even_digits = digits[-2::-2]
    checksum = 0
    checksum += sum(odd_digits)
    for d in even_digits:
        checksum += sum(digits_of(d*2))
    checksum = checksum % 10
    return checksum
 
def is_luhn_valid(card_number):
    is_valid = luhn_checksum(card_number) == 0
    return is_valid

def calculate_luhn(partial_card_number):
    checksum = luhn_checksum(int(partial_card_number) * 10)
    if checksum == 0:
        check_digit = 0
    else:
        check_digit = 10 - checksum
    return check_digit
