from uuid import UUID

import pytest
from django.db import models

from django_models.models.generic import UUIDModel
from testapp.models import (
    TestSortOrderModel,
    TestSerializerModel,
    TestUUIDSerializerModel,
    TestCodeModel,
    TestSlugModel,
    TestActiveModel,
    TestTimestampedModel,
)

pytestmark = pytest.mark.django_db


class TestSortOrderModelFunctionality:
    """Test SortOrderModel functionality."""

    def test_get_next_sort_order_with_existing_sort_order(self):
        """Test _get_next_sort_order when instance already has sort_order > 0."""
        # Create instance with existing sort_order
        instance = TestSortOrderModel(name="test", sort_order=5)

        # Should return existing sort_order
        result = instance._get_next_sort_order()
        assert result == 5

    def test_get_next_sort_order_with_zero_sort_order(self):
        """Test _get_next_sort_order when instance has sort_order = 0."""
        # Create and save an instance first
        TestSortOrderModel.objects.create(name="first", sort_order=10)

        # Create new instance with sort_order = 0
        instance = TestSortOrderModel(name="test", sort_order=0)

        # Should return next available sort_order
        result = instance._get_next_sort_order()
        assert result == 11

    def test_get_next_sort_order_no_existing_instances(self):
        """Test _get_next_sort_order when no instances exist."""
        # Ensure no instances exist
        TestSortOrderModel.objects.all().delete()

        # Create new instance
        instance = TestSortOrderModel(name="test")

        # Should return 1
        result = instance._get_next_sort_order()
        assert result == 1

    def test_get_next_sort_order_with_existing_instances_no_sort_order(self):
        """Test _get_next_sort_order when existing instances have no sort_order."""
        # Create instance with sort_order = 0
        TestSortOrderModel.objects.create(name="first", sort_order=0)

        # Create new instance
        instance = TestSortOrderModel(name="test")

        # Should return 1 since existing instance has sort_order = 0
        result = instance._get_next_sort_order()
        assert result == 1

    def test_get_next_sort_order_with_multiple_instances(self):
        """Test _get_next_sort_order with multiple existing instances."""
        # Create multiple instances
        TestSortOrderModel.objects.create(name="first", sort_order=5)
        TestSortOrderModel.objects.create(name="second", sort_order=10)
        TestSortOrderModel.objects.create(name="third", sort_order=3)

        # Create new instance
        instance = TestSortOrderModel(name="test")

        # Should return highest sort_order + 1 (10 + 1 = 11)
        result = instance._get_next_sort_order()
        assert result == 11


class TestSerializerModelFunctionality:
    """Test SerializerModel functionality."""

    def test_serialize_with_uuid_field(self):
        """Test serialize method with UUID field conversion."""
        # Create instance with UUID
        instance = TestUUIDSerializerModel.objects.create(name="test")

        # Serialize the instance
        data = instance.serialize()

        # Check that UUID field is converted to string
        assert isinstance(instance.id, UUID)
        assert isinstance(data["id"], str)
        assert data["name"] == "test"

    def test_serialize_without_uuid_field(self):
        """Test serialize method without UUID fields."""
        # Create instance without UUID
        instance = TestSerializerModel.objects.create(name="test")

        # Serialize the instance
        data = instance.serialize()

        # Check basic serialization
        assert data["name"] == "test"
        assert "id" in data

    def test_serializer_property(self):
        """Test serializer property returns correct serializer class."""
        instance = TestSerializerModel.objects.create(name="test")

        # Get serializer
        serializer_class = instance.serializer

        # Should be a ModelSerializer subclass
        assert hasattr(serializer_class, "Meta")
        assert serializer_class.Meta.model == instance
        assert serializer_class.Meta.fields == "__all__"


class TestCodeModelFunctionality:
    """Test CodeModel functionality."""

    def test_code_model_creation(self):
        """Test CodeModel creates instances with code field."""
        instance = TestCodeModel.objects.create(name="test")

        # Should have a code field
        assert hasattr(instance, "code")
        assert instance.code is not None
        assert len(instance.code) > 0


class TestSlugModelFunctionality:
    """Test SlugModel functionality."""

    def test_slug_model_creation(self):
        """Test SlugModel creates instances with slug field."""
        instance = TestSlugModel(name="test", slug="test-slug")

        # Should have a slug field
        assert hasattr(instance, "slug")
        assert instance.slug == "test-slug"


class TestActiveModelFunctionality:
    """Test ActiveModel functionality."""

    def test_active_model_creation(self):
        """Test ActiveModel creates instances with is_active field."""
        instance = TestActiveModel.objects.create(name="test")

        # Should have is_active field defaulting to True
        assert hasattr(instance, "is_active")
        assert instance.is_active is True

    def test_active_model_inactive(self):
        """Test ActiveModel with is_active=False."""
        instance = TestActiveModel.objects.create(name="test", is_active=False)

        # Should be inactive
        assert instance.is_active is False


class TestTimestampedModelFunctionality:
    """Test TimestampedModel functionality."""

    def test_timestamped_model_creation(self):
        """Test TimestampedModel creates instances with timestamp fields."""
        instance = TestTimestampedModel.objects.create(name="test")

        # Should have timestamp fields
        assert hasattr(instance, "created_at")
        assert hasattr(instance, "updated_at")
        assert instance.created_at is not None
        assert instance.updated_at is not None


class TestUUIDModelFunctionality:
    """Test UUIDModel functionality."""

    def test_uuid_model_creation(self):
        """Test UUIDModel creates instances with UUID primary key."""

        # Create a test model that inherits from UUIDModel
        class TestUUIDOnlyModel(UUIDModel):
            name = models.CharField(max_length=100)

            class Meta:
                app_label = "testapp"

        instance = TestUUIDOnlyModel(name="test")

        # Should have UUID id field
        assert hasattr(instance, "id")
        # ID should be None before saving (auto-generated on save)
        assert instance.id is None or isinstance(instance.id, UUID)
