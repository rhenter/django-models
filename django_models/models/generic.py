from functools import partial
from typing import Any, Dict, Type
from uuid import UUID

from django.db import models
from django.utils.functional import cached_property
from django.utils.translation import gettext_lazy as _
from rest_framework.serializers import ModelSerializer

from django_models.fields import UUIDPrimaryKeyField
from django_models.utils.generators import generate_random_code

# Partial function to generate 8-character random codes
generate_code = partial(generate_random_code, length=8)


class BaseModel(models.Model):
    """
    Base abstract model class for all models in the django-models library.

    This is the foundation class that other abstract models inherit from.
    It provides a common base for all model mixins and can be used as a
    starting point for custom models.
    """

    class Meta:
        abstract = True


class ActiveModel(models.Model):
    """
    Abstract model that adds an 'is_active' field for soft enabling/disabling records.

    This model provides a boolean field to mark records as active or inactive,
    which is useful for implementing soft deletion patterns or temporarily
    disabling records without removing them from the database.

    Attributes:
        is_active (BooleanField): Boolean field indicating if the record is active
    """

    is_active = models.BooleanField(_("Active"), default=True)

    class Meta:
        abstract = True


class CodeModel(models.Model):
    """
    Abstract model that adds a unique code field with automatic generation.

    This model provides a CharField that automatically generates a unique
    8-character random code for each instance. The code is useful for
    creating human-readable identifiers or public IDs that don't expose
    internal database IDs.

    Attributes:
        code (CharField): Unique 8-character code automatically generated
    """

    code = models.CharField(
        max_length=32,
        default=generate_code,
        verbose_name=_("Model code"),
        unique=True,
    )

    class Meta:
        abstract = True


class SerializerModel(BaseModel):
    """
    Abstract model that provides automatic serialization capabilities using DRF.

    This model adds methods to automatically serialize model instances using
    Django REST Framework's ModelSerializer. It creates a dynamic serializer
    for the model and provides a serialize method that converts UUID fields
    to strings for JSON compatibility.
    """

    @cached_property
    def serializer(self) -> Type[ModelSerializer]:
        """
        Create and return a dynamic ModelSerializer for this model.

        Returns:
            A ModelSerializer class configured for this model instance
        """

        class SelfSerializer(ModelSerializer):
            class Meta:
                pass

        SelfSerializer.Meta.model = self
        SelfSerializer.Meta.fields = "__all__"
        return SelfSerializer

    def serialize(self) -> Dict[str, Any]:
        """
        Serialize the model instance to a dictionary.

        This method uses the dynamic serializer to convert the model instance
        to a dictionary, with special handling for UUID fields which are
        converted to strings for JSON compatibility.

        Returns:
            Dictionary representation of the model instance
        """
        data = self.serializer(self).data

        for key, value in data.items():
            if isinstance(value, UUID):
                data[key] = str(value)
        return data

    class Meta:
        abstract = True


class SlugModel(BaseModel):
    """
    Abstract model that adds a slug field for URL-friendly identifiers.

    This model provides a SlugField that can be used to create URL-friendly
    versions of model names or titles. Slugs are commonly used in URLs
    to make them more readable and SEO-friendly.

    Attributes:
        slug (SlugField): URL-friendly identifier field
    """

    slug = models.SlugField(max_length=16)

    class Meta:
        abstract = True


class SortOrderModel(models.Model):
    """
    Abstract model that adds sorting capabilities to models.

    This model provides a sort_order field that can be used to manually
    order model instances. It includes a helper method to automatically
    calculate the next sort order value.

    Attributes:
        sort_order (PositiveIntegerField): Field for manual ordering of instances
    """

    sort_order = models.PositiveIntegerField(
        default=0, blank=False, null=False, verbose_name=_("Sort")
    )

    class Meta:
        abstract = True

    def _get_next_sort_order(self) -> int:
        """
        Calculate the next sort order value for this model.

        If the instance already has a sort_order value, it returns that value.
        Otherwise, it finds the highest sort_order value in the database
        and returns the next value.

        Returns:
            The next sort order value to use
        """
        if self.sort_order and self.sort_order > 0:
            return self.sort_order

        # Get the highest sort_order value from existing instances
        last_instance = type(self).objects.order_by("-sort_order").first()
        if last_instance and last_instance.sort_order:
            return last_instance.sort_order + 1

        return 1


class TimestampedModel(models.Model):
    """
    Abstract model that adds automatic timestamp fields for creation and updates.

    This model provides created_at and updated_at fields that are automatically
    managed by Django. The created_at field is set when the instance is first
    saved, and updated_at is updated every time the instance is saved.

    Attributes:
        created_at (DateTimeField): Timestamp when the instance was created
        updated_at (DateTimeField): Timestamp when the instance was last updated
    """

    created_at = models.DateTimeField(
        db_index=True, auto_now_add=True, verbose_name=_("Created at")
    )
    updated_at = models.DateTimeField(auto_now=True, verbose_name=_("Updated at"))

    class Meta:
        abstract = True


class UUIDModel(BaseModel):
    """
    Abstract model that uses UUID as the primary key instead of auto-incrementing integers.

    This model replaces the default integer primary key with a UUID field,
    which provides better security by not exposing sequential IDs and
    better scalability for distributed systems.

    Attributes:
        id (UUIDPrimaryKeyField): UUID primary key field
    """

    id = UUIDPrimaryKeyField()

    class Meta:
        abstract = True
