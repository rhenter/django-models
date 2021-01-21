from functools import partial
from uuid import UUID

from django.db import models
from django.utils.functional import cached_property
from django.utils.translation import gettext_lazy as _
from rest_framework.serializers import ModelSerializer

from django_models.fields import UUIDPrimaryKeyField
from django_models.utils.generators import generate_random_code

generate_code = partial(generate_random_code, length=16)


class BaseModel(models.Model):
    class Meta:
        abstract = True


class ActiveModel(models.Model):
    active = models.BooleanField(_('Active'), default=True)

    class Meta:
        abstract = True


class CodeModel(models.Model):
    code = models.CharField(
        max_length=32,
        default=generate_code,
        verbose_name=_('Model code'),
        unique=True,
    )

    class Meta:
        abstract = True


class SerializerModel(BaseModel):

    @cached_property
    def serializer(self):
        class SelfSerializer(ModelSerializer):
            class Meta:
                pass

        SelfSerializer.Meta.model = self
        SelfSerializer.Meta.fields = '__all__'
        return SelfSerializer

    def serialize(self):
        data = self.serializer(self).data

        for key, value in data.items():
            if isinstance(value, UUID):
                data[key] = str(value)
        return data

    class Meta:
        abstract = True


class SlugModel(BaseModel):
    slug = models.SlugField(max_length=16)

    class Meta:
        abstract = True


class TimestampedModel(BaseModel):
    created_at = models.DateTimeField(
        auto_now_add=True, verbose_name=_('Created at')
    )
    updated_at = models.DateTimeField(
        auto_now=True, verbose_name=_('Updated at')
    )

    class Meta:
        abstract = True


class UUIDModel(BaseModel):
    id = UUIDPrimaryKeyField()

    class Meta:
        abstract = True
