from django.forms import ValidationError
from django.forms.fields import CharField
from django.utils.translation import gettext_lazy as _

from .validators import validate_cpf, validate_cnpj
from .utils import is_equal


class InvalidValuesField:
    invalid_values = ()

    def clean(self, value):
        value = super().clean(value)
        if value in self.invalid_values:
            raise ValidationError(_("Invalid number."))
        return value


class CPFField(InvalidValuesField, CharField):
    invalid_values = ('00000000191',)

    def __init__(self, max_length=14, min_length=11, *args, **kwargs):
        super().__init__(max_length=max_length, min_length=min_length, *args, **kwargs)

    def clean(self, value):
        value = super().clean(value)
        code = validate_cpf(value)
        if not code or is_equal(code):
            raise ValidationError(_("Invalid CPF number."))
        return code


class CNPJField(InvalidValuesField, CharField):
    invalid_values = (
        '00000000000000', '22222222000191', '33333333000191', '44444444000191',
        '55555555000191', '66666666000191', '77777777000191', '88888888000191',
        '99999999000191'
    )

    def __init__(self, min_length=14, max_length=18, *args, **kwargs):
        super().__init__(max_length=max_length, min_length=min_length, *args, **kwargs)

    def clean(self, value):
        value = super().clean(value)
        code = validate_cnpj(value)
        if not code or is_equal(code):
            raise ValidationError(_("Invalid CNPJ number."))
        return code

