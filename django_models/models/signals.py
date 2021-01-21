import inspect

from django.db import models, transaction
from django.utils import timezone

from .generic import SerializerModel
from .managers import SignalsManager, SoftDeleteSignalsManager


class SignalsModel(SerializerModel):
    SOFT_DELETE = False

    class Meta:
        abstract = True

    objects = SignalsManager()

    def get_context(self, **kwargs):
        force_insert = kwargs.get('force_insert', False)
        creation_conditions = (
            self.id is None,
            force_insert is True
        )
        context = {'is_creation': any(creation_conditions)}
        context.update(kwargs)
        return context

    def trigger_event(self, event_name, context):
        for attribute in dir(self):
            if attribute.startswith(event_name):
                method = getattr(self, attribute)
                if inspect.ismethod(method):
                    method(context)

    def save(self, *args, **kwargs):
        force_insert = kwargs.get('force_insert', False)
        context = self.get_context(force_insert=force_insert)

        with transaction.atomic():
            self.trigger_event('pre_save', context)
            super().save(*args, **kwargs)
            self.trigger_event('post_save', context)

    def delete(self, *args, **kwargs):
        context = self.get_context()

        if self.SOFT_DELETE and not kwargs.pop('hard_delete', False):
            self.deleted_at = timezone.now()
            self.is_deleted = True
            self.save()
            return

        with transaction.atomic():
            self.trigger_event('pre_delete', context)
            super().delete(*args, **kwargs)
            self.trigger_event('post_delete', context)


class SoftDeleteSignalModel(SignalsModel):
    SOFT_DELETE = True
    deleted_at = models.DateTimeField(blank=True, null=True)
    is_deleted = models.BooleanField(default=False)

    objects = SoftDeleteSignalsManager()
    all_objects = SoftDeleteSignalsManager(show_deleted=True)

    class Meta:
        abstract = True

    def hard_delete(self):
        super().delete(hard_delete=True)

    def restore(self):
        self.deleted_at = None
        self.is_deleted = False
        self.save()
