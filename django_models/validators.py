from typing import Union, List
from django.core.validators import EMPTY_VALUES

from .utils import is_equal
from .utils.string import digits_only

# Sequential values that are invalid for CPF validation
SEQ_VALUES: List[str] = [
    "00000000000",
    "11111111111",
    "22222222222",
    "33333333333",
    "44444444444",
    "55555555555",
    "66666666666",
    "77777777777",
    "88888888888",
    "99999999999",
]


def dv_maker(v: int) -> int:
    """
    Calculate the verification digit for Brazilian documents.

    This is a helper function used in CPF and CNPJ validation algorithms
    to calculate the verification digits.

    Args:
        v: The calculated sum value from the document validation algorithm

    Returns:
        The verification digit (0 if v < 2, otherwise 11 - v)
    """
    if v >= 2:
        return 11 - v
    return 0


def validate_cpf(value: str) -> Union[str, bool]:
    """
    Validate a Brazilian CPF (Cadastro de Pessoas Físicas) number.

    The CPF is an 11-digit number used to identify individuals in Brazil.
    This function validates the CPF using the official algorithm that checks
    the verification digits.

    Args:
        value: CPF number as a string. Can be in the format XXX.XXX.XXX-XX
               or as an 11-digit number string.

    Returns:
        The original value if valid, False if invalid.

    Examples:
        >>> validate_cpf('123.456.789-09')
        '123.456.789-09'
        >>> validate_cpf('12345678909')
        '12345678909'
        >>> validate_cpf('00000000000')
        False
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

    # Calculate first verification digit
    r1 = range(10, 1, -1)
    new_1dv = sum([i * int(value[idx]) for idx, i in enumerate(r1)])
    new_1dv = dv_maker(new_1dv % 11)
    value = value[:-2] + str(new_1dv) + value[-1]

    # Calculate second verification digit
    r2 = range(11, 1, -1)
    new_2dv = sum([i * int(value[idx]) for idx, i in enumerate(r2)])
    new_2dv = dv_maker(new_2dv % 11)
    value = value[:-1] + str(new_2dv)

    # Validate verification digits
    if value[-2:] != orig_dv:
        return False

    # Check for repeated digits (invalid CPF pattern)
    if value.count(value[0]) == 11:
        return False

    return orig_value


def validate_cnpj(value: str) -> Union[str, bool]:
    """
    Validate a Brazilian CNPJ (Cadastro Nacional da Pessoa Jurídica) number.

    The CNPJ is a 14-digit number used to identify companies in Brazil.
    This function validates the CNPJ using the official algorithm that checks
    the verification digits.

    Args:
        value: CNPJ number as a string. Can be in the format XX.XXX.XXX/XXXX-XX
               or as a 14-digit number string.

    Returns:
        The original value if valid, False if invalid, empty string if empty value.

    Examples:
        >>> validate_cnpj('11.222.333/0001-81')
        '11.222.333/0001-81'
        >>> validate_cnpj('11222333000181')
        '11222333000181'
        >>> validate_cnpj('00000000000000')
        False
    """
    if value in EMPTY_VALUES:
        return ""

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

    # Calculate first verification digit
    list1 = list(range(5, 1, -1))
    list2 = list(range(9, 1, -1))
    new_1dv = sum([i * int(value[idx]) for idx, i in enumerate(list1 + list2)])
    new_1dv = dv_maker(new_1dv % 11)
    value = value[:-2] + str(new_1dv) + value[-1]

    # Calculate second verification digit
    list3 = list(range(6, 1, -1))
    new_2dv = sum([i * int(value[idx]) for idx, i in enumerate(list3 + list2)])
    new_2dv = dv_maker(new_2dv % 11)
    value = value[:-1] + str(new_2dv)

    # Validate verification digits
    if value[-2:] != orig_dv:
        return False

    return orig_value
