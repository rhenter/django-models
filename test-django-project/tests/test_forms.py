import pytest
from django.forms import ValidationError

from django_models.forms import CNPJField, CPFField


@pytest.mark.parametrize("value", ["21552411273", "215.524,112-73"])
def test_cpf_field_valid(value):
    assert CPFField().clean(value) == value


@pytest.mark.parametrize(
    "value",
    CPFField.invalid_values + ("12345678901", "12345678901!@", "1234567890112312312"),
)
def test_cpf_field_invalid(value):
    with pytest.raises(ValidationError):
        CPFField().clean(value)


@pytest.mark.parametrize("value", ["09654773000166", "09.654.773/0001-66"])
def test_cnpj_field_valid(value):
    assert CNPJField().clean(value) == value


@pytest.mark.parametrize(
    "value",
    CNPJField.invalid_values + ("12345678901234", "1234567890112312312", "      "),
)
def test_cnpj_field_invalid(value):
    with pytest.raises(ValidationError):
        CNPJField().clean(value)
