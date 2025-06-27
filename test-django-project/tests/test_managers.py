import pytest

from django_models.models.managers import SoftDeleteSignalsManager
from testapp.models import TestSignalsModel, TestSoftDeleteModel

pytestmark = pytest.mark.django_db


class TestSignalsManagerFunctionality:
    """Test SignalsManager functionality."""

    def test_create_method(self):
        """Test SignalsManager create method."""
        instance = TestSignalsModel.objects.create(name="test")

        assert instance.name == "test"
        assert instance.pk is not None

    def test_initialize_model_instance(self):
        """Test SignalsManager initialize_model_instance method."""
        manager = TestSignalsModel.objects
        instance = manager.initialize_model_instance(name="test")

        assert isinstance(instance, TestSignalsModel)
        assert instance.name == "test"
        assert instance.pk is None  # Not saved yet


class TestSoftDeleteQuerySetFunctionality:
    """Test SoftDeleteQuerySet functionality."""

    def test_soft_delete(self):
        """Test soft delete functionality."""
        # Create test instance
        instance = TestSoftDeleteModel.objects.create(name="test")
        assert instance.is_deleted is False
        assert instance.deleted_at is None

        # Soft delete
        TestSoftDeleteModel.objects.filter(pk=instance.pk).delete()

        # Refresh from database
        instance.refresh_from_db()
        assert instance.is_deleted is True
        assert instance.deleted_at is not None

    def test_hard_delete(self):
        """Test hard delete functionality."""
        # Create test instance
        instance = TestSoftDeleteModel.objects.create(name="test")
        instance_id = instance.pk

        # Hard delete
        deleted, rows_count = TestSoftDeleteModel.objects.filter(
            pk=instance.pk
        ).hard_delete()

        # Should be completely removed from database
        assert not TestSoftDeleteModel.all_objects.filter(pk=instance_id).exists()

    def test_hard_delete_with_sliced_queryset(self):
        """Test hard delete with sliced queryset raises assertion error."""
        TestSoftDeleteModel.objects.create(name="test1")
        TestSoftDeleteModel.objects.create(name="test2")

        # Try to hard delete with limit - should raise AssertionError
        with pytest.raises(AssertionError):
            TestSoftDeleteModel.objects.all()[:1].hard_delete()

    def test_hard_delete_after_values(self):
        """Test hard delete after values() raises TypeError."""
        TestSoftDeleteModel.objects.create(name="test")

        # Try to hard delete after values() - should raise TypeError
        with pytest.raises(TypeError):
            TestSoftDeleteModel.objects.values("name").hard_delete()

    def test_hard_delete_after_values_list(self):
        """Test hard delete after values_list() raises TypeError."""
        TestSoftDeleteModel.objects.create(name="test")

        # Try to hard delete after values_list() - should raise TypeError
        with pytest.raises(TypeError):
            TestSoftDeleteModel.objects.values_list("name").hard_delete()

    def test_restore(self):
        """Test restore functionality."""
        # Create and soft delete instance
        instance = TestSoftDeleteModel.objects.create(name="test")
        TestSoftDeleteModel.objects.filter(pk=instance.pk).delete()

        # Verify it's deleted
        instance.refresh_from_db()
        assert instance.is_deleted is True

        # Restore
        TestSoftDeleteModel.all_objects.filter(pk=instance.pk).restore()

        # Verify it's restored
        instance.refresh_from_db()
        assert instance.is_deleted is False
        assert instance.deleted_at is None

    def test_queryset_repr(self):
        """Test QuerySet __repr__ method."""
        # Create multiple instances
        for i in range(25):  # More than REPR_OUTPUT_SIZE (20)
            TestSoftDeleteModel.objects.create(name=f"test{i}")

        # Get queryset representation
        qs = TestSoftDeleteModel.objects.all()
        repr_str = repr(qs)

        # Should contain truncation message
        assert "...(remaining elements truncated)..." in repr_str
        assert repr_str.startswith("<QuerySet")

    def test_queryset_repr_small(self):
        """Test QuerySet __repr__ method with small dataset."""
        # Create few instances
        for i in range(5):
            TestSoftDeleteModel.objects.create(name=f"test{i}")

        # Get queryset representation
        qs = TestSoftDeleteModel.objects.all()
        repr_str = repr(qs)

        # Should not contain truncation message
        assert "...(remaining elements truncated)..." not in repr_str
        assert repr_str.startswith("<QuerySet")


class TestSoftDeleteSignalsManagerFunctionality:
    """Test SoftDeleteSignalsManager functionality."""

    def test_manager_initialization_show_deleted_false(self):
        """Test manager initialization with show_deleted=False."""
        manager = SoftDeleteSignalsManager(show_deleted=False)
        assert manager.show_deleted is False

    def test_manager_initialization_show_deleted_true(self):
        """Test manager initialization with show_deleted=True."""
        manager = SoftDeleteSignalsManager(show_deleted=True)
        assert manager.show_deleted is True

    def test_get_queryset_exclude_deleted(self):
        """Test get_queryset excludes deleted items by default."""
        # Create normal and deleted instances
        normal = TestSoftDeleteModel.objects.create(name="normal")
        deleted = TestSoftDeleteModel.objects.create(name="deleted")
        TestSoftDeleteModel.objects.filter(pk=deleted.pk).delete()

        # Default manager should exclude deleted
        qs = TestSoftDeleteModel.objects.all()
        assert normal in qs
        assert deleted not in qs

    def test_get_queryset_include_deleted(self):
        """Test get_queryset includes deleted items when show_deleted=True."""
        # Create normal and deleted instances
        normal = TestSoftDeleteModel.all_objects.create(name="normal")
        deleted = TestSoftDeleteModel.all_objects.create(name="deleted")
        TestSoftDeleteModel.all_objects.filter(pk=deleted.pk).delete()

        # all_objects manager should include deleted
        qs = TestSoftDeleteModel.all_objects.all()
        assert normal in qs
        assert deleted in qs

    def test_manager_delete(self):
        """Test manager delete method."""
        instance = TestSoftDeleteModel.objects.create(name="test")

        # Delete using manager
        TestSoftDeleteModel.objects.delete()

        # Should be soft deleted
        instance.refresh_from_db()
        assert instance.is_deleted is True

    def test_manager_hard_delete(self):
        """Test manager hard_delete method."""
        instance = TestSoftDeleteModel.objects.create(name="test")
        instance_id = instance.pk

        # Hard delete using manager
        TestSoftDeleteModel.objects.hard_delete()

        # Should be completely removed
        assert not TestSoftDeleteModel.all_objects.filter(pk=instance_id).exists()

    def test_manager_restore(self):
        """Test manager restore method."""
        instance = TestSoftDeleteModel.objects.create(name="test")
        TestSoftDeleteModel.objects.filter(pk=instance.pk).delete()

        # Restore using manager
        TestSoftDeleteModel.all_objects.restore()

        # Should be restored
        instance.refresh_from_db()
        assert instance.is_deleted is False

    def test_filter_with_is_deleted(self):
        """Test filter method with is_deleted parameter."""
        # Create normal and deleted instances
        normal = TestSoftDeleteModel.objects.create(name="normal")
        deleted = TestSoftDeleteModel.objects.create(name="deleted")
        TestSoftDeleteModel.objects.filter(pk=deleted.pk).delete()

        # Filter with is_deleted=True should return deleted items
        deleted_qs = TestSoftDeleteModel.objects.filter(is_deleted=True)
        assert deleted in deleted_qs
        assert normal not in deleted_qs

        # Filter with is_deleted=False should return normal items
        normal_qs = TestSoftDeleteModel.objects.filter(is_deleted=False)
        assert normal in normal_qs
        assert deleted not in normal_qs

    def test_filter_without_is_deleted(self):
        """Test filter method without is_deleted parameter."""
        instance = TestSoftDeleteModel.objects.create(name="test")

        # Regular filter should work normally
        qs = TestSoftDeleteModel.objects.filter(name="test")
        assert instance in qs

    def test_trash_method(self):
        """Test trash method returns deleted items."""
        # Create normal and deleted instances
        normal = TestSoftDeleteModel.objects.create(name="normal")
        deleted = TestSoftDeleteModel.objects.create(name="deleted")
        TestSoftDeleteModel.objects.filter(pk=deleted.pk).delete()

        # Trash should return only deleted items
        trash_qs = TestSoftDeleteModel.objects.trash()
        assert deleted in trash_qs
        assert normal not in trash_qs
