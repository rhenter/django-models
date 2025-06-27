import uuid
from typing import Any

from django.core.validators import RegexValidator
from django.db import models
from django.db.models import Model


class UUIDPrimaryKeyField(models.UUIDField):
    """
    A UUID field that automatically sets itself as the primary key.

    This field automatically configures itself as:
    - primary_key=True
    - unique=True
    - editable=False

    It generates a UUID4 value automatically when the model instance is saved
    if no value has been set.
    """

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        """
        Initialize the UUID primary key field.

        Args:
            *args: Variable length argument list passed to parent class
            **kwargs: Arbitrary keyword arguments passed to parent class
        """
        kwargs["primary_key"] = True
        kwargs["unique"] = True
        kwargs["editable"] = False
        super().__init__(*args, **kwargs)

    def pre_save(self, model_instance: Model, add: bool) -> uuid.UUID:
        """
        Generate a UUID4 value before saving if none exists.

        Args:
            model_instance: The model instance being saved
            add: True if this is a new instance being added

        Returns:
            The UUID value that will be saved
        """
        value = super().pre_save(model_instance, add)

        if value is None:
            value = uuid.uuid4()
            setattr(model_instance, self.attname, value)

        return value


class CharFieldDigitsOnly(models.CharField):
    """
    A CharField that only accepts digits and whitespace characters.

    This field validates that the input contains only digits (0-9) and
    whitespace characters. It's useful for fields like phone numbers,
    postal codes, or other numeric identifiers that may contain spaces.
    """

    default_validators = [
        RegexValidator(
            r"^([\s\d]+)$", "Only digits and whitespace characters are allowed."
        )
    ]
