Generic Models
==============

You just need to add to your template to get the behaviors below. Use as many models as you want.

ActiveModel
-----------

Model with is_active boolean field

Usage:

.. code-block:: python

    class YourModel(ActiveModel)
       ...


CodeModel
---------

Model with a code field that automatically generates a hash of 16 characters by default. Useful to identify your record in a more humane way

Usage:

.. code-block:: python

    class YourModel(CodeModel)
       ...


SerializerModel
---------------

Model with serialize method making possible serializer your instance data returning a dict.

Usage:

.. code-block:: python

    from django_models.models import SerializerModel
    ...

    class YourModel(SerializerModel)
        name = models.CharField(max_length=255)
        ...

Example of a instance from a Model using the SerializerModel

.. code-block:: python

    instance.serialize()
    {
        'id': 1,
        'name': 'Test'
    }


SlugModel
---------

Model with a slug field. Useful to use in urls or nominal references

Usage:

.. code-block:: python

    class YourModel(SlugModel)
       ...




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

Model that uses the id field as a UUID. Useful to be able to have a unique identifier without worrying about sequences.


Usage:

.. code-block:: python

    from django_models.models import UUIDModel
    ...

    class YourModel(UUIDModel)
        ...



