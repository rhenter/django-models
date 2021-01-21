Fields
======


UUIDPrimaryKeyField
-------------------

Field to use UUID as Primary Key of your model instead of the sequential

usage:

.. code-block:: python

    from django_models.fields import UUIDPrimaryKeyField

    ...
    class TestModel(models.Model):
        id = UUIDPrimaryKeyField()
        ...


CharFieldDigitsOnly
-------------------

Field to use only digits but with zero on left.

usage:

.. code-block:: python

    from django_models.fields import CharFieldDigitsOnly

    ...
    class TestModel(models.Model):
        code = CharFieldDigitsOnly(max_length=10)
        ...
