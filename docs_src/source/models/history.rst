History Model
=============

Model to save changes to specific fields any time the template is saved

Required fields
---------------

- history_model

    Field with the model where will save the changes

- history_parent_field_name

    Field used in the foreign key in the template where the changes will be stored.
    The default value is **parent**


Example
-------

.. code-block:: python

    from django_models.models import HistoryModel

    class HistoryTestModel(models.Model):
        parent = models.ForeignKey('TestHistoryModel', related_name='history', on_delete=models.CASCADE)
        name = models.CharField(max_length=128)
        email = models.CharField(max_length=32, default='example@example.com')

    class TestHistoryModel(HistoryModel):
        history_model = HistoryTestModel
        name = models.CharField(max_length=128)
        email = models.CharField(max_length=32, default='example@example.com')
        description = models.CharField(max_length=32,blank=True)


Note: In this example, only the **name** and **email** will only be saved in the change history.
