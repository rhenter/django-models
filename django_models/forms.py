from typing import Any, Tuple
from django.forms import ValidationError
from django.forms.fields import CharField
from django.utils.translation import gettext_lazy as _

from .validators import validate_cpf, validate_cnpj
from .utils import is_equal


class InvalidValuesField:
    """
    A mixin class for form fields that need to validate against a list of invalid values.

    This class provides functionality to check if a field value is in a predefined
    list of invalid values and raise a ValidationError if it is.

    Attributes:
        invalid_values: A tuple of values that are considered invalid for this field.
    """

    invalid_values: Tuple[str, ...] = ()

    def clean(self, value: str) -> str:
        """
        Clean and validate the field value against invalid values.

        Args:
            value: The value to validate

        Returns:
            The cleaned value if valid

        Raises:
            ValidationError: If the value is in the invalid_values tuple
        """
        value = super().clean(value)  # type: ignore
        if value in self.invalid_values:
            raise ValidationError(_("Invalid number."))
        return value


class CPFField(InvalidValuesField, CharField):
    """
    A form field for Brazilian CPF (Cadastro de Pessoas Físicas) validation.

    This field validates CPF numbers using the official Brazilian algorithm.
    It accepts CPF numbers in various formats (with or without dots and dashes)
    and validates them according to the CPF verification digit algorithm.

    Attributes:
        invalid_values: Tuple of known invalid CPF values that should be rejected
    """

    invalid_values: Tuple[str, ...] = ("00000000191",)

    def __init__(
        self, max_length: int = 14, min_length: int = 11, *args: Any, **kwargs: Any
    ) -> None:
        """
        Initialize the CPF field.

        Args:
            max_length: Maximum length for the field (default: 14 for formatted CPF)
            min_length: Minimum length for the field (default: 11 for unformatted CPF)
            *args: Variable length argument list passed to parent class
            **kwargs: Arbitrary keyword arguments passed to parent class
        """
        super().__init__(max_length=max_length, min_length=min_length, *args, **kwargs)

    def clean(self, value: str) -> str:
        """
        Clean and validate the CPF value.

        Args:
            value: The CPF value to validate

        Returns:
            The validated CPF value

        Raises:
            ValidationError: If the CPF is invalid
        """
        value = super().clean(value)
        code = validate_cpf(value)
        if not code or is_equal(code):
            raise ValidationError(_("Invalid CPF number."))
        return code


class CNPJField(InvalidValuesField, CharField):
    """
    A form field for Brazilian CNPJ (Cadastro Nacional da Pessoa Jurídica) validation.

    This field validates CNPJ numbers using the official Brazilian algorithm.
    It accepts CNPJ numbers in various formats (with or without dots, slashes and dashes)
    and validates them according to the CNPJ verification digit algorithm.

    Attributes:
        invalid_values: Tuple of known invalid CNPJ values that should be rejected
    """

    invalid_values: Tuple[str, ...] = (
        "00000000000000",
        "22222222000191",
        "33333333000191",
        "44444444000191",
        "55555555000191",
        "66666666000191",
        "77777777000191",
        "88888888000191",
        "99999999000191",
    )

    def __init__(
        self, min_length: int = 14, max_length: int = 18, *args: Any, **kwargs: Any
    ) -> None:
        """
        Initialize the CNPJ field.

        Args:
            min_length: Minimum length for the field (default: 14 for unformatted CNPJ)
            max_length: Maximum length for the field (default: 18 for formatted CNPJ)
            *args: Variable length argument list passed to parent class
            **kwargs: Arbitrary keyword arguments passed to parent class
        """
        super().__init__(max_length=max_length, min_length=min_length, *args, **kwargs)

    def clean(self, value: str) -> str:
        """
        Clean and validate the CNPJ value.

        Args:
            value: The CNPJ value to validate

        Returns:
            The validated CNPJ value

        Raises:
            ValidationError: If the CNPJ is invalid
        """
        value = super().clean(value)
        code = validate_cnpj(value)
        if not code or is_equal(code):
            raise ValidationError(_("Invalid CNPJ number."))
        return code
