from typing import Any, Dict, Optional

from django.db import models, transaction
from django.utils import timezone

from .generic import SerializerModel
from .managers import SignalsManager, SoftDeleteSignalsManager


class SignalsModel(SerializerModel):
    """
    Abstract model that provides custom signal handling for model operations.

    This model extends the standard Django model save/delete operations with
    custom event triggers. It allows you to define methods that will be called
    before and after save/delete operations by naming them with specific prefixes:
    - pre_save_*: Called before saving
    - post_save_*: Called after saving
    - pre_delete_*: Called before deletion
    - post_delete_*: Called after deletion

    Attributes:
        SOFT_DELETE (bool): Whether this model supports soft deletion
        objects (SignalsManager): Custom manager for signal-aware operations
    """

    SOFT_DELETE = False

    class Meta:
        abstract = True

    objects = SignalsManager()

    def get_context(self, **kwargs: Any) -> Dict[str, Any]:
        """
        Generate context information for signal events.

        Creates a context dictionary that includes information about whether
        this is a creation operation and any additional kwargs passed.

        Args:
            **kwargs: Additional context information

        Returns:
            Dictionary containing context information for signal handlers
        """
        force_insert = kwargs.get("force_insert", False)
        creation_conditions = (self.id is None, force_insert is True)
        context = {"is_creation": any(creation_conditions)}
        context.update(kwargs)
        return context

    def trigger_event(self, event_name: str, context: Dict[str, Any]) -> None:
        """
        Trigger all methods that match the given event name pattern.

        Searches for methods on this instance that start with the event_name
        and calls them with the provided context. This allows for flexible
        event handling by simply defining methods with the right prefix.

        Args:
            event_name: The event prefix to search for (e.g., 'pre_save')
            context: Context dictionary to pass to event handlers
        """
        for attribute in dir(self):
            if attribute.startswith(event_name):
                method = getattr(self, attribute)
                if callable(method) and not attribute.startswith("_"):
                    try:
                        method(context)
                    except Exception:
                        # Log the error but don't break the flow
                        # You might want to use proper logging here
                        pass

    def save(self, *args: Any, **kwargs: Any) -> None:
        """
        Save the model instance with custom signal handling.

        This method wraps the standard Django save operation with custom
        pre_save and post_save event triggers. The pre_save events are
        called within a database transaction.

        Args:
            *args: Variable length argument list passed to parent save
            **kwargs: Arbitrary keyword arguments passed to parent save
        """
        force_insert = kwargs.get("force_insert", False)
        context = self.get_context(force_insert=force_insert)

        with transaction.atomic():
            self.trigger_event("pre_save", context)
            super().save(*args, **kwargs)

        self.trigger_event("post_save", context)

    def delete(self, *args: Any, **kwargs: Any) -> Optional[tuple]:
        """
        Delete the model instance with custom signal handling.

        This method wraps the standard Django delete operation with custom
        pre_delete and post_delete event triggers. If SOFT_DELETE is True,
        it performs a soft delete instead of actual deletion.

        Args:
            *args: Variable length argument list passed to parent delete
            **kwargs: Arbitrary keyword arguments passed to parent delete

        Returns:
            Tuple of (number_of_objects_deleted, {model_label: count}) or None for soft delete
        """
        context = self.get_context()

        if self.SOFT_DELETE and not kwargs.pop("hard_delete", False):
            self.deleted_at = timezone.now()  # type: ignore
            self.is_deleted = True  # type: ignore
            self.save()
            return None

        with transaction.atomic():
            self.trigger_event("pre_delete", context)
            result = super().delete(*args, **kwargs)
            self.trigger_event("post_delete", context)
            return result


class SoftDeleteSignalModel(SignalsModel):
    """
    Abstract model that provides soft deletion capabilities with signal handling.

    This model extends SignalsModel to provide soft deletion functionality.
    Instead of actually deleting records from the database, it marks them
    as deleted using the is_deleted flag and sets a deletion timestamp.

    The model provides two managers:
    - objects: Returns only non-deleted instances
    - all_objects: Returns all instances including deleted ones

    Attributes:
        SOFT_DELETE (bool): Always True for this model
        deleted_at (DateTimeField): Timestamp when the record was soft deleted
        is_deleted (BooleanField): Flag indicating if the record is deleted
        objects (SoftDeleteSignalsManager): Manager that excludes deleted records
        all_objects (SoftDeleteSignalsManager): Manager that includes all records
    """

    SOFT_DELETE = True
    deleted_at = models.DateTimeField(blank=True, null=True)
    is_deleted = models.BooleanField(default=False)

    objects = SoftDeleteSignalsManager()
    all_objects = SoftDeleteSignalsManager(show_deleted=True)

    class Meta:
        abstract = True

    def hard_delete(self) -> tuple:
        """
        Permanently delete the record from the database.

        This method bypasses the soft delete mechanism and actually
        removes the record from the database. Use with caution.

        Returns:
            Tuple of (number_of_objects_deleted, {model_label: count})
        """
        return super().delete(hard_delete=True)

    def restore(self) -> None:
        """
        Restore a soft-deleted record.

        This method clears the deletion flag and timestamp, effectively
        "undeleting" the record and making it visible through the default
        manager again.
        """
        self.deleted_at = None
        self.is_deleted = False
        self.save()
