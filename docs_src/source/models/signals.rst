Signals Model
=============

Model that makes it possible to add any task before or after you save, update or delete your model, just adding a method in your model

Usage:

Pre-save
~~~~~~~~

Note: This will be made before you save your model

.. code-block:: python

    from django_models.models import SignalsModel
    ...

    class YourModel(SignalsModel)
        ...
        def pre_save(self):
            do_something()



Pos-save
~~~~~~~~

Note: This will be made after you save your model

.. code-block:: python

    from django_models.models import SignalsModel
    ...

    class YourModel(SignalsModel)
        ...
        def pos_save(self):
            do_something()


Pre-delete
~~~~~~~~~~

Note: This will be made before you delete your model

.. code-block:: python

    from django_models.models import SignalsModel
    ...

    class YourModel(SignalsModel)
        ...
        def pre_delete(self):
            do_something()




Pos-delete
~~~~~~~~~~

Note: This will be made after you delete your model

.. code-block:: python

    from django_models.models import SignalsModel
    ...

    class YourModel(SignalsModel)
        ...
        def pos_delete(self):
            do_something()


