=============
Django Models
=============

|PyPI latest| |PyPI Version| |PyPI License|  |CicleCI Status| |Coverage| |Docs|

Django Models é uma biblioteca com vários templates úteis para Django para ajudá-lo a tornar seus templates inteligentes ou com menos código

Requirements
============

- Python 3.x
- Django 1.11 ou mais novo

Features
========

Generic Models
--------------

- ActiveModel

  Modelo com campo boolean is_active

- CodeModel

  Modelo com um campo code que gera automaticamente um hash de 16 caracteres por padrão. Muito util para identificar seu registro de forma mais humanizada

- SerializerModel

  Modelo com o metodo serialize que retorna um dict com todas as informações da instância sem precisar de um serializador configurado.

Como Instalar
Examplo:

Vamos la!delo**
.. code-block:: python

    from django_models.models import SignalsModel
    ...

    class YourModel(SignalsModel)
        name = models.CharField(max_length=255)
        ...

**Uso**

.. code-block:: python

    In[1]: from . import YourModel
    In[2]: instance = YourModel.objects.first()
    In[3]: user.serialize()
    Out[3]: {'id': 1, 'name': 'primeiro registro', ...}

- SlugModel

  Modelo com um campo slug. util para se usar em urls ou referencias nominais

- TimestampedModel

  Template with DateTime, created_at and updated_at fields. Useful to control when any changes were made.

- UUIDModel

  Modelo que usa o campo id como um UUID. Util para poder ter um identificador único sem se preocupar com sequenciais.

- Signals

Usando o SignalsModel, permite que você manipule ou execute um evento de acordo com os Signals do Django.

Quando Salvar:
 - pre_save (Antes de Salvar)
 - post_save (Depois de Salvar)

Quando Apagar:
 - pre_delete (Antes de Apagar)
 - post_delete (Depois de Apagar)

Examplo usando o signal Pre-save

.. code-block:: python

    from django_models.models import SignalsModel
    ...

    class YourModel(SignalsModel)
        ...
        def pre_save(self):
            do_something()


- History models

  Modelo que permite rastrear cada alteração feita na instância ao salvar para gerar um Historico de modificações da instância

Como Instalar
=============

Vamos la!
---------

Você pode instalar o Django Models usando pip:

.. code:: shell

    $ pip install django-models


Se preferir instalar usando o codigo, pegue o endereço do repositorio git do GitHub e rode o setup.py

.. code:: shell

    $ git clone git@github.com:rhenter/django_models.git
    $ cd django_models
    $ python setup.py install


Configurando
------------

To enable `django_models` in your project you need to add it to `INSTALLED_APPS` in your projects
`settings.py` file:

Para habilitar o `django_models` no seu projeto você precisa adiciona-lo ao `INSTALLED_APPS` no arquivo `settings.py` do seu projeto:

.. code-block:: python

    INSTALLED_APPS = (
        ...
        'django_models',
        ...
    )


Documentação
============

Confira a ultima versão da documento do ``django-models`` em `Read the Docs <http://django-models.readthedocs.io/en/latest/>`_

Contribuição
============

Por favor envie pull requests, são muito apreciados.


1. Faço o Fork do repositorio `repository <https://github.com/rhenter/django_models>`_ no GitHub.
2. Crie uma branch fora da master e commit as suas modificações.
3. Instale as dependências. ``pip install -r requirements-dev.txt``
4. Instale o pre-commit. ``pre-commit install``
5. Rode os testes com ``cd test-django-project; py.test -vv -s``
6. Crie um Pull Request com a sua contribuição


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
