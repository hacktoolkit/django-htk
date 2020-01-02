import copy


DIGITS = '0123456789'
LETTERS = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz'
BASE_62_LIST = DIGITS + LETTERS
BASE_52_LIST = copy.copy(LETTERS)


def build_base_dict(base_list):
    base_dict = dict((c, i) for i, c in enumerate(base_list))
    return base_dict


BASE_62_DICT = build_base_dict(BASE_62_LIST)
BASE_52_DICT = build_base_dict(BASE_52_LIST)


def base_encode(integer, base_list):
    base = len(base_list)
    value = ''
    while integer != 0:
        value = base_list[integer % base] + value
        integer //= base

    return value


def base_decode(encoded, reverse_base_dict):
    base = len(reverse_base_dict)
    value = 0
    for i, c in enumerate(reversed(encoded)):
        value += (base ** i) * reverse_base_dict[c]

    return value


def base62_encode(integer, base_list=BASE_62_LIST):
    value = base_encode(integer, base_list)
    return value


def base62_decode(encoded, base_dict=BASE_62_DICT):
    value = base_decode(encoded, base_dict)
    return value


def base52_encode(integer, base_list=BASE_52_LIST):
    value = base_encode(integer, base_list)
    return value


def base52_decode(encoded, base_dict=BASE_52_DICT):
    value = base_decode(encoded, base_dict)
    return value
