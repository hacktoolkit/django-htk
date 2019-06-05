def is_alpha(c):
    result = ord('A') <= ord(c.upper()) <= ord('Z')
    return result


def is_ascii(c):
    result = 0 <= ord(c) <= 127
    return result


def is_ascii_extended(c):
    result = 128 <= ord(c) <= 255
    return result
