=============
Django Models
=============

|PyPI latest| |PyPI Version| |PyPI License|  |GitHub Actions Status| |Coverage| |Docs| |Open Source? Yes!|

Django Models é uma biblioteca com vários Modelos úteis para Django para ajudá-lo a tornar seus templates inteligentes ou com menos código

Requirements
============

- Python 3.8 ou mais novo
- Django 1.11 ou mais novo

Features
========

Generic Models
--------------

- ActiveModel

  Modelo com campo boolean is_active

- CodeModel

  Modelo com um campo code que gera automaticamente um hash de 16 caracteres por padrão. Muito útil para identificar seu registro de forma mais humanizada

History models
--------------

- HistoryModel

  Modelo que permite rastrear cada alteração feita na instância ao salvar para gerar um Histórico de modificações da instância

- SerializerModel

  Modelo com o método serialize que retorna um dict com todas as informações da instância sem precisar de um serializador configurado.

.. code-block:: python

    from django_models.models import SerializerModel
    ...

    class YourModel(SerializerModel)
        name = models.CharField(max_length=255)
        ...

**Uso**

.. code-block:: python

    In[1]: from . import YourModel
    In[2]: instance = YourModel.objects.first()
    In[3]: user.serialize()
    Out[3]: {'id': 1, 'name': 'primeiro registro', ...}

- SlugModel

  Modelo com um campo slug. Útil para se usar em urls ou referências nominais

- TimestampedModel

  Modelo com os campos Datetime, created_at and updated_at. Úteis para controlar quando uma instância foi criada ou alterada.

- UUIDModel

  Modelo que usa o campo id como um UUID. Útil para poder ter um identificador único sem se preocupar com sequenciais.


Signals Models
--------------

- SignalsModel

Usando o SignalsModel, permite que você manipule ou execute um evento de acordo com os Signals do Django.

Quando Salvar:
 - pre_save (Antes de Salvar)
 - post_save (Depois de Salvar)

Quando Apagar:
 - pre_delete (Antes de Apagar)
 - post_delete (Depois de Apagar)

Exemplo usando o signal Pre-save

.. code-block:: python

    from django_models.models import SignalsModel
    ...

    class YourModel(SignalsModel)
        ...
        def pre_save(self):
            do_something()


Soft Delete Signal Model
------------------------

- SoftDeleteSignalModel Models

  É o SignalsModel com soft delete implementado. Permite que nada que você apague seja realmente apagado do sistema e de fácil recuperação


Como Instalar
=============

Vamos lá!
---------

Você pode instalar o Django Models usando pip:

.. code:: shell

    $ pip install django-models


Se preferir instalar usando o código, pegue o endereço do repositório git do GitHub e rode o setup.py

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

Confira a última versão da documentação do ``django-models`` em `GitHub Pages <https://rhenter.github.io/django-models/>`_

Contribuição
============

Por favor envie pull requests, são muito apreciados.


1. Faça o Fork do repositório `repository <https://github.com/rhenter/django_models>`_ no GitHub.
2. Crie uma branch fora da master e commit as suas modificações.
3. Instale as dependências. ``pip install -r requirements-dev.txt``
4. Instale o pre-commit. ``pre-commit install``
5. Rode os testes com ``cd test-django-project; py.test -vv -s``
6. Crie um Pull Request com a sua contribuição


.. |Docs| image:: https://img.shields.io/static/v1?label=DOC&message=GitHub%20Pages&color=%3CCOLOR%3E
   :target: https://rhenter.github.io/django-models/
.. |PyPI Version| image:: https://img.shields.io/pypi/pyversions/django-models.svg?maxAge=60
   :target: https://pypi.python.org/pypi/django-models
.. |PyPI License| image:: https://img.shields.io/pypi/l/django-models.svg?maxAge=120
   :target: https://github.com/rhenter/django-models/blob/master/LICENSE
.. |PyPI latest| image:: https://img.shields.io/pypi/v/django-models.svg?maxAge=120
   :target: https://pypi.python.org/pypi/django-models
.. |GitHub Actions Status| image:: https://github.com/rhenter/django-models/workflows/Tests/badge.svg
   :target: https://github.com/rhenter/django-models/actions/workflows/ci.yml
.. |Coverage| image:: https://codecov.io/gh/rhenter/django-models/branch/master/graph/badge.svg
   :target: https://codecov.io/gh/rhenter/django-models
.. |Open Source? Yes!| image:: https://badgen.net/badge/Open%20Source%20%3F/Yes%21/blue?icon=github
   :target: https://github.com/rhenter/django-models
