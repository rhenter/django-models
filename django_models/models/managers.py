from django.db import models, transaction
from django.db.models import QuerySet
from django.db.models.deletion import Collector
from django.utils import timezone

REPR_OUTPUT_SIZE = 20


class SignalsManager(models.Manager):

    def create(self, **kwargs):
        model_instance = self.initialize_model_instance(**kwargs)
        with transaction.atomic():
            model_instance.save()
        return model_instance

    def initialize_model_instance(self, **kwargs):
        return self.model(**kwargs)


class SoftDeleteQuerySet(QuerySet):
    def delete(self):
        return super().update(deleted_at=timezone.now(), is_deleted=True)

    def hard_delete(self):
        """Delete the records in the current QuerySet."""
        self._not_support_combined_queries('delete')
        assert not self.query.is_sliced, \
            "Cannot use 'limit' or 'offset' with delete."

        if self._fields is not None:
            raise TypeError("Cannot call delete() after .values() or .values_list()")

        del_query = self._chain()

        # The delete is actually 2 queries - one to find related objects,
        # and one to delete. Make sure that the discovery of related
        # objects is performed on the same database as the deletion.
        del_query._for_write = True

        # Disable non-supported fields.
        del_query.query.select_for_update = False
        del_query.query.select_related = False
        del_query.query.clear_ordering(force_empty=True)

        collector = Collector(using=del_query.db)
        collector.collect(del_query)
        deleted, _rows_count = collector.delete()

        # Clear the result cache, in case this QuerySet gets reused.
        self._result_cache = None
        return deleted, _rows_count

    def restore(self):
        return super().update(deleted_at=None, is_deleted=False)

    def __repr__(self):
        data = list(self[:REPR_OUTPUT_SIZE + 1])
        if len(data) > REPR_OUTPUT_SIZE:
            data[-1] = "...(remaining elements truncated)..."
        return '<QuerySet %r>' % data


class SoftDeleteSignalsManager(SignalsManager):
    def __init__(self, *args, **kwargs):
        self.show_deleted = kwargs.pop('show_deleted', False)
        super().__init__(*args, **kwargs)

    def get_queryset(self):
        if self.show_deleted:
            return SoftDeleteQuerySet(self.model, using=self._db)
        return SoftDeleteQuerySet(self.model, using=self._db).exclude(is_deleted=True)

    def delete(self):
        return self.get_queryset().delete()

    def hard_delete(self):
        return self.get_queryset().hard_delete()

    def restore(self):
        return self.get_queryset().restore()

    def filter(self, *args, **kwargs):
        if 'is_deleted' in kwargs:
            qs = SoftDeleteQuerySet(self.model, using=self._db)
            return qs.filter(*args, **kwargs)
        return super().filter(*args, **kwargs)

    def trash(self):
        return self.filter(is_deleted=True)
