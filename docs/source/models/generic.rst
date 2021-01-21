Generic Models
==============

You just need to add to your template to get the behaviors below. Use as many models as you want.


SlugModel
---------

Model with a slugField already implemented

Usage:

.. code-block:: python

    class YourModel(SlugModel)
       ...


SerializerModel
---------------

Model with serialize method making possible serializer your instance data returning a dict.

Usage:

.. code-block:: python

    from django_models.models import SerializerModel
    ...

    class YourModel(SerializerModel)
        ...

Example of a instance from a Model using the SerializerModel

.. code-block:: python

    instance.serialize()
    {
        'id': 1,
        'name': 'Test'
    }


TimestampedModel
----------------

Model with created_at and updated_at fields to let you know when your instance wore created and updated

Usage:

.. code-block:: python

    from django_models.models import TimestampedModel
    ...

    class YourModel(TimestampedModel)
        ...

UUIDModel
---------

Model with UUIDPrimaryKeyField already implemented


Usage:

.. code-block:: python

    from django_models.models import UUIDModel
    ...

    class YourModel(UUIDModel)
        ...



