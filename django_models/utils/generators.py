import hashlib
import random
import string
import time
from datetime import datetime, timedelta

from django.utils.crypto import get_random_string


def generate_random_code(length=10):
    allowed = string.ascii_uppercase + string.digits
    code = get_random_string(length=length, allowed_chars=allowed)
    return code


def generate_md5_hashcode(key_word):
    keyword = '{}-{}'.format(key_word, time.time())
    hashcode = hashlib.md5(keyword.encode('utf-8')).hexdigest()
    return hashcode


def generate_datetime(min_year=1900, max_year=datetime.now().year):
    """Generate a datetime."""
    start = datetime(min_year, 1, 1, 00, 00, 00)
    years = max_year - min_year + 1
    end = start + timedelta(days=365 * years)
    return start + (end - start) * random.random()


def generate_cpf():
    cpf = [random.randint(0, 9) for x in range(9)]

    for _ in range(2):
        val = sum([(len(cpf) + 1 - i) * v for i, v in enumerate(cpf)]) % 11

        cpf.append(11 - val if val > 1 else 0)

    return '%s%s%s.%s%s%s.%s%s%s-%s%s' % tuple(cpf)


def generate_cnpj():
    def calculate_special_digit(l):
        digit = 0

        for i, v in enumerate(l):
            digit += v * (i % 8 + 2)

        digit = 11 - digit % 11

        return digit if digit < 10 else 0

    cnpj = [1, 0, 0, 0] + [random.randint(0, 9) for x in range(8)]

    for _ in range(2):
        cnpj = [calculate_special_digit(cnpj)] + cnpj

    return '%s%s.%s%s%s.%s%s%s/%s%s%s%s-%s%s' % tuple(cnpj[::-1])
