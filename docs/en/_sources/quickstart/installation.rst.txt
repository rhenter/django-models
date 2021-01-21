Installation
============

Requirements
------------

- Python 3.x
- Django 1.11 or later


Install
-------

You can get Django Models by using pip:

.. code:: shell

    $ pip install django-models


If you want to install it from source, grab the git repository from Gitlab and run setup.py:

.. code:: shell

    $ git clone git@github.com:rhenter/django_models.git
    $ cd django_models
    $ python setup.py install


Enable
------

To enable `django_models` in your project you need to add it to `INSTALLED_APPS` in your projects
`settings.py` file:

.. code-block:: python

    INSTALLED_APPS = (
        ...
        'django_models',
        ...
    )
