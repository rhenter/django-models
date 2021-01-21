import pytest
from uuid import UUID

from django_models.models.exceptions import HistoryModelNotSetError
from testapp.models import TestSignalsModel, TestHistoryModel, TestHistoryFail, TestModel

pytestmark = pytest.mark.django_db


def test_history_model_creation():
    obj = TestHistoryModel.objects.create(name='test 01')
    history = obj.history.all()[0]

    assert obj.history.count() == 1
    assert obj.name == history.name
    assert obj.email == history.email


def test_history_model_update():
    # Create:
    obj = TestHistoryModel.objects.create(name='test 01')

    # Update:
    obj.status = 'step 2'
    obj.name = 'Lorem Mister Ipsum'
    obj.email = 'exmachine@example.com'
    obj.save()

    history = obj.history.all()[1]

    assert obj.history.count() == 2
    assert obj.name == history.name
    assert obj.email == history.email


def test_history_model_unrelated_fields():
    # Create:
    obj = TestHistoryModel.objects.create(name='test 01')
    obj.description = 'Be like water my friend.'
    obj.save()

    history = obj.history.all()[1]

    assert obj.history.count() == 2

    with pytest.raises(AttributeError):
        history.description


def test_history_model_invalid():
    with pytest.raises(HistoryModelNotSetError):
        TestHistoryFail.objects.create(name='test 01')


def test_signals_model_save_with_create():
    obj = TestSignalsModel.objects.create(name='test 01')
    assert obj.debug_info['pre_save_handler_called'] == 1
    assert obj.debug_info['post_save_handler_called'] == 1

    assert obj.debug_info['pre_update_handler_called'] == 0
    assert obj.debug_info['post_update_handler_called'] == 0

    assert obj.debug_info['pre_delete_handler_called'] == 0
    assert obj.debug_info['post_delete_handler_called'] == 0

    assert obj.pk is not None


def test_signals_model_serialize_method():
    obj = TestModel.objects.create(name='test 01')
    data = obj.serialize()

    assert isinstance(obj.id, UUID)
    assert not isinstance(data['id'], UUID)


def test_signals_model_is_creation_context_value():
    obj = TestSignalsModel(name='test 01')
    assert obj.get_context()['is_creation'] is True

    obj2 = TestSignalsModel(name='test 02')
    obj2.id = 1
    assert obj.get_context()['is_creation'] is True


def test_signals_model_delete():
    TestSignalsModel.objects.create(name='test 01')
    obj = TestSignalsModel.objects.get(name='test 01')
    obj.delete()

    assert obj.debug_info['pre_save_handler_called'] == 0
    assert obj.debug_info['post_save_handler_called'] == 0

    assert obj.debug_info['pre_update_handler_called'] == 0
    assert obj.debug_info['post_update_handler_called'] == 0

    assert obj.debug_info['pre_delete_handler_called'] == 1
    assert obj.debug_info['post_delete_handler_called'] == 1
