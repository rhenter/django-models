from django.core.validators import EMPTY_VALUES

from .utils import is_equal
from .utils.string import digits_only

SEQ_VALUES = [
    '00000000000',
    '11111111111',
    '22222222222',
    '33333333333',
    '44444444444',
    '55555555555',
    '66666666666',
    '77777777777',
    '88888888888',
    '99999999999'
]


def dv_maker(v):
    if v >= 2:
        return 11 - v
    return 0


def validate_cpf(value):
    """
    Value can be either a string in the format XXX.XXX.XXX-XX or
    an 11-digit number.
    """
    if value in EMPTY_VALUES or value in SEQ_VALUES:
        return False
    orig_value = value[:]
    if not value.isdigit():
        value = digits_only(value)
        if not value:
            return False

    if is_equal(value):
        return False

    if len(value) != 11:
        return False
    orig_dv = value[-2:]

    r1 = range(10, 1, -1)
    new_1dv = sum([i * int(value[idx]) for idx, i in enumerate(r1)])
    new_1dv = dv_maker(new_1dv % 11)
    value = value[:-2] + str(new_1dv) + value[-1]
    r2 = range(11, 1, -1)
    new_2dv = sum([i * int(value[idx]) for idx, i in enumerate(r2)])
    new_2dv = dv_maker(new_2dv % 11)
    value = value[:-1] + str(new_2dv)
    if value[-2:] != orig_dv:
        return False
    if value.count(value[0]) == 11:
        return False
    return orig_value


def validate_cnpj(value):
    """
    Value can be either a string in the format XX.XXX.XXX/XXXX-XX or
    a group of 14 characters.
    """
    if value in EMPTY_VALUES:
        return ''
    orig_value = value[:]
    if not value.isdigit():
        value = digits_only(value)
        if not value:
            return False

    if is_equal(value):
        return False

    if len(value) != 14:
        return False
    orig_dv = value[-2:]

    list1 = list(range(5, 1, -1))
    list2 = list(range(9, 1, -1))
    new_1dv = sum([i * int(value[idx]) for idx, i in enumerate(list1 + list2)])
    new_1dv = dv_maker(new_1dv % 11)
    value = value[:-2] + str(new_1dv) + value[-1]
    list3 = list(range(6, 1, -1))
    new_2dv = sum([i * int(value[idx]) for idx, i in enumerate(list3 + list2)])
    new_2dv = dv_maker(new_2dv % 11)
    value = value[:-1] + str(new_2dv)
    if value[-2:] != orig_dv:
        return False
    return orig_value
