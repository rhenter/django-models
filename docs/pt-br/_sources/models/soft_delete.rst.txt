Soft Delete Signal Model
========================

It is the SignalsModel with soft delete implemented. Allows nothing you delete to be really deleted from the system and easy to recover

Usage in the Model:


.. code-block:: python

    from django_models.models import SoftDeleteSignalModel
    ...

    class YourModel(SoftDeleteSignalModel)
        ...
        def pre_save(self):
            do_something()



- Restore

.. code-block:: python

    In[1]: from . import YourModel
    In[2]: instance = YourModel.objects.get(id=1)
    In[3]: instance.delete()
    In[3]: YourModel.objects.filter(id=1).restore()

