import uuid

from django.core.validators import RegexValidator
from django.db import models


class UUIDPrimaryKeyField(models.UUIDField):

    def __init__(self, *args, **kwargs):
        kwargs['primary_key'] = True
        kwargs['unique'] = True
        kwargs['editable'] = False
        super().__init__(*args, **kwargs)

    def pre_save(self, model_instance, add):
        value = super().pre_save(model_instance, add)

        if value is None:
            value = uuid.uuid4()
            setattr(model_instance, self.attname, value)

        return value


class CharFieldDigitsOnly(models.CharField):
    default_validators = [RegexValidator(r'^([\s\d]+)$', 'Only digits characters')]
