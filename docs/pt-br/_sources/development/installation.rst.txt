Development Installation
========================

Requirements
------------

- Python 3.x
- Django 1.11 or later


Development install
-------------------

After forking or checking out:

.. code-block:: bash

    $ cd django-models/
    $ pip install -r requirements-dev.txt
    $ pre-commit install

The requirements-dev are only used for development, so we can easily
install/track dependencies required to run the tests using continuous
integration platforms.

The official entrypoint for distritubution is the ``requirements.txt`` which
contains the minimum requirements to execute the tests.


Running tests
-------------

.. code-block:: bash

    $ make test

or:

.. code-block:: bash

    $ cd test-django-project/
    $ py.test -vv -s

Generating documentation
------------------------

.. code-block:: bash

    $ cd docs/
    $ make html
