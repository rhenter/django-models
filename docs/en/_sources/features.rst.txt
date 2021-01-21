Generic Models
~~~~~~~~~~~~~~

- SerializerModel

  Model to return a dict with all data of your django instance without a serializer.


Example:

**Your Model**

.. code-block:: python

    from django_models.models import SignalsModel
    ...

    class YourModel(SignalsModel)
        name = models.CharField(max_length=255)
        ...

**Usage**

.. code-block:: python

    In[1]: from . import YourModel
    In[2]: instance = YourModel.objects.first()
    In[3]: user.serialize()
    Out[3]: {'id': 1, 'name': 'first record', ...}

- SlugModel

  Model with a slug field. Useful to use in urls or nominal references

- TimestampedModel

  Model with the DateTime, created_at and updated_at fields. Useful to control when any changes were made.

- UUIDModel

  Model that uses the id field as a UUID. Useful to be able to have a unique identifier without worrying about sequences.

History Model
~~~~~~~~~~~~~

- History models

  Model that track each save to generate a History Changes of a record

Signals Models
~~~~~~~~~~~~~~

With SignalModel it allows you to handle or execute an event according to Django's Signals.

On Save:
  - pre_save (Before Saving)
  - post_save (After saving)

On Erase:
  - pre_delete (Before Erasing)
  - post_delete (After Deleting)

Example using Pre-save signal

Note: This will be made before you save your model

.. code-block:: python

    from django_models.models import SignalsModel
    ...

    class YourModel(SignalsModel)
        ...
        def pre_save(self):
            do_something()


Soft Delete Signal Model
~~~~~~~~~~~~~~~~~~~~~~~~

It is the SignalsModel with soft delete implemented. Allows nothing you delete to be really deleted from the system and easy to recover

