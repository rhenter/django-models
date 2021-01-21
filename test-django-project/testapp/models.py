from django.db import models

from django_models.models import UUIDModel, HistoryModel, SignalsModel, TimestampedModel, SerializerModel
from django_models.fields import CharFieldDigitsOnly


class TestModel(UUIDModel, TimestampedModel, SerializerModel):
    name = models.CharField(max_length=128)


class TestSignalsModel(SignalsModel, UUIDModel):
    name = models.CharField(max_length=128)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.debug_info = {
            'pre_save_handler_called': 0,
            'post_save_handler_called': 0,
            'pre_update_handler_called': 0,
            'post_update_handler_called': 0,
            'pre_delete_handler_called': 0,
            'post_delete_handler_called': 0
        }

    def pre_save(self, context):
        self.debug_info['pre_save_handler_called'] += 1

    def post_save(self, context):
        self.debug_info['post_save_handler_called'] += 1

    def pre_update(self, context):
        self.debug_info['pre_update_handler_called'] += 1

    def post_update(self, context):
        self.debug_info['post_update_handler_called'] += 1

    def pre_delete(self, context):
        self.debug_info['pre_delete_handler_called'] += 1

    def post_delete(self, context):
        self.debug_info['post_delete_handler_called'] += 1


class HistoryTestModel(UUIDModel):
    parent = models.ForeignKey('TestHistoryModel', related_name='history', on_delete=models.CASCADE)
    name = models.CharField(max_length=128)
    email = models.CharField(max_length=32, default='example@example.com')


class TestHistoryModel(HistoryModel, SignalsModel):
    history_model = HistoryTestModel
    name = models.CharField(max_length=128)
    email = models.CharField(max_length=32, default='example@example.com')
    description = models.CharField(max_length=32, default='Lorem Ipsum', blank=True)


class TestHistoryFail(HistoryModel):
    name = models.CharField(max_length=128)


class TestDigitsOnlyField(models.Model):
    digits_only_field = CharFieldDigitsOnly(max_length=5)
