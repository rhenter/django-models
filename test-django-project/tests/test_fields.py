import pytest
import uuid

from django.forms import ValidationError

from testapp.models import TestModel, TestDigitsOnlyField

pytestmark = pytest.mark.django_db


def test_uuid_primary_key_field():
    obj = TestModel(name='Name')
    assert obj.pk is None
    obj.save()
    assert obj.pk is not None
    assert isinstance(obj.pk, uuid.UUID)


@pytest.mark.parametrize('value', ('1', '123', '00123', '000'))
def test_char_field_only_digits_valid(value):
    assert not TestDigitsOnlyField(digits_only_field=value).full_clean()


@pytest.mark.parametrize('value', ('a', '12db', '1.23', '123-4'))
def test_char_field_only_digits_invalid(value):
    with pytest.raises(ValidationError) as exc:
        TestDigitsOnlyField(digits_only_field=value).full_clean()
    assert 'digits_only_field' in exc.value.error_dict
