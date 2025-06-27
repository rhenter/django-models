from django.db import models

from django_models.fields import CharFieldDigitsOnly
from django_models.models import (
    HistoryModel,
    SignalsModel,
)
from django_models.models.generic import (
    SortOrderModel,
    SerializerModel,
    UUIDModel,
    CodeModel,
    SlugModel,
    ActiveModel,
    TimestampedModel,
)
from django_models.models.managers import SignalsManager, SoftDeleteSignalsManager


class SampleModel(UUIDModel, TimestampedModel, SerializerModel):
    name = models.CharField(max_length=128)


class SampleSignalsModel(SignalsModel, UUIDModel):
    name = models.CharField(max_length=128)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.debug_info = {
            "pre_save_handler_called": 0,
            "post_save_handler_called": 0,
            "pre_update_handler_called": 0,
            "post_update_handler_called": 0,
            "pre_delete_handler_called": 0,
            "post_delete_handler_called": 0,
        }

    def pre_save(self, context):
        self.debug_info["pre_save_handler_called"] += 1

    def post_save(self, context):
        self.debug_info["post_save_handler_called"] += 1

    def pre_update(self, context):
        self.debug_info["pre_update_handler_called"] += 1

    def post_update(self, context):
        self.debug_info["post_update_handler_called"] += 1

    def pre_delete(self, context):
        self.debug_info["pre_delete_handler_called"] += 1

    def post_delete(self, context):
        self.debug_info["post_delete_handler_called"] += 1


class HistoryTestModel(UUIDModel):
    parent = models.ForeignKey(
        "SampleHistoryModel", related_name="history", on_delete=models.CASCADE
    )
    name = models.CharField(max_length=128)
    email = models.CharField(max_length=32, default="example@example.com")


class SampleHistoryModel(HistoryModel, SignalsModel):
    history_model = HistoryTestModel
    name = models.CharField(max_length=128)
    email = models.CharField(max_length=32, default="example@example.com")
    description = models.CharField(max_length=32, default="Lorem Ipsum", blank=True)


class SampleHistoryFail(HistoryModel):
    name = models.CharField(max_length=128)


class SampleDigitsOnlyField(models.Model):
    digits_only_field = CharFieldDigitsOnly(max_length=5)


class TestSortOrderModel(SortOrderModel):
    name = models.CharField(max_length=100)


class TestSerializerModel(SerializerModel):
    name = models.CharField(max_length=100)


class TestUUIDSerializerModel(SerializerModel, UUIDModel):
    name = models.CharField(max_length=100)


class TestCodeModel(CodeModel):
    name = models.CharField(max_length=100)


class TestSlugModel(SlugModel):
    name = models.CharField(max_length=100)


class TestActiveModel(ActiveModel):
    name = models.CharField(max_length=100)


class TestTimestampedModel(TimestampedModel):
    name = models.CharField(max_length=100)


class TestSignalsModel(models.Model):
    name = models.CharField(max_length=100)

    objects = SignalsManager()


class TestSoftDeleteModel(models.Model):
    name = models.CharField(max_length=100)
    is_deleted = models.BooleanField(default=False)
    deleted_at = models.DateTimeField(null=True, blank=True)

    objects = SoftDeleteSignalsManager()
    all_objects = SoftDeleteSignalsManager(show_deleted=True)
