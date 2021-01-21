=============
Django Models
=============

|PyPI latest| |PyPI Version| |PyPI License|  |CicleCI Status| |Coverage| |Docs|

Django Models is Library with several useful templates for Django to help you make your templates smart or with less code

Requirements
============

- Python 3.x
- Django 1.11 or later

Features
========

Generic Models
--------------

- ActiveModel

  Model with is_active boolean field

- CodeModel

  Model with 32 characters hash code to use to identify your record

- SerializerModel

  Model to return a dict with all data of your django instance without a serializaer.


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

  Model with slug field

- TimestampedModel

  Model with created_at and updated_at DateTime fields

- UUIDModel

  Model using the field id as UUID

- Signals

With SignalModel it allows you to handle or execute an event according to Django's Signals.

On save:
 - pre_save
 - post_save

On Delete
 - pre_delete
 - post_delete

Example using Pre-save signal

Note: This will be made before you save your model

.. code-block:: python

    from django_models.models import SignalsModel
    ...

    class YourModel(SignalsModel)
        ...
        def pre_save(self):
            do_something()


- History models

  Model that track each save to generate a History Changes of a record

How to install
==============

Getting It
----------

You can get Django Models by using pip:

.. code:: shell

    $ pip install django-models


If you want to install it from source, grab the git repository from Gitlab and run setup.py:

.. code:: shell

    $ git clone git@github.com:rhenter/django_models.git
    $ cd django_models
    $ python setup.py install


Installing It
-------------

To enable `django_models` in your project you need to add it to `INSTALLED_APPS` in your projects
`settings.py` file:

.. code-block:: python

    INSTALLED_APPS = (
        ...
        'django_models',
        ...
    )


Documentation
=============

Check out the latest ``django-models`` documentation at `Read the Docs <http://django-models.readthedocs.io/en/latest/>`_


Contributing
============

Please send pull requests, very much appreciated.


1. Fork the `repository <https://github.com/rhenter/django_models>`_ on GitHub.
2. Make a branch off of master and commit your changes to it.
3. Install requirements. ``pip install -r requirements-dev.txt``
4. Install pre-commit. ``pre-commit install``
5. Run the tests with ``cd test-django-project; py.test -vv -s``
6. Create a Pull Request with your contribution


.. |Docs| image:: https://readthedocs.org/projects/django-models/badge/?version=latest
   :target: http://django-models.readthedocs.org/en/latest/?badge=latest
.. |PyPI Version| image:: https://img.shields.io/pypi/pyversions/django-models.svg?maxAge=60
   :target: https://pypi.python.org/pypi/django-models
.. |PyPI License| image:: https://img.shields.io/pypi/l/django-models.svg?maxAge=120
   :target: https://github.com/rhenter/django-models/blob/master/LICENSE
.. |PyPI latest| image:: https://img.shields.io/pypi/v/django-models.svg?maxAge=120
   :target: https://pypi.python.org/pypi/django-models
.. |CicleCI Status| image:: https://circleci.com/gh/rhenter/django-models.svg?style=svg
   :target: https://circleci.com/gh/rhenter/django-models
.. |Coverage| image:: https://codecov.io/gh/rhenter/django-models/branch/master/graph/badge.svg
   :target: https://codecov.io/gh/rhenter/django-models
