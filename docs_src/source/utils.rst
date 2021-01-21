Utils
=====

generate_md5_hashcode
---------------------

Generates an MD5 hash code from a key word

Usage:

.. code-block:: python

    In[0]: from django_models.utils import generate_md5_hashcode
    In[1]: generate_md5_hashcode('test')
    Out[1]: '39df5136522809aafdf726f1a8a7d00d'


generate_random_code
--------------------

Generates an random code with a specific length

Usage:

.. code-block:: python

    In[0]: from django_models.utils import generate_random_code
    In[1]: generate_random_code(16)    # with 16 length
    Out[1]: 'U7Q2M1FW79WIGSW0'
    In[2]: generate_random_code(10)    # with 10 length
    Out[2]: 'D2U2PHUSBD'

generate_datetime
--------------------

Generates an random datetime

Usage:

.. code-block:: python

    In[0]: from django_models.utils import generate_datetime
    In[1]: generate_datetime()
    Out[1]: datetime.datetime(1995, 4, 6, 21, 42, 32, 955163)
    In[2]: generate_datetime(min_year=2019)    # with min_year
    Out[2]: datetime.datetime(2019, 9, 26, 1, 17, 38, 303408)

is_equal
--------

Checks if the word are formed with the same character

Usage:

.. code-block:: python

    In[0]: from django_models.utils import is_equal
    In[1]: is_equal('asdfgh')
    Out[1]: False
    In[2]: is_equal('aaaaaaaaaa')
    Out[2]: True

sanitize_digits
---------------

Removes all non digits characters from a string

Usage:

.. code-block:: python

    In[0]: from django_models.utils import sanitize_digits
    In[1]: sanitize_digits('123.123.123-23')
    Out[1]: '12312312323'
    In[2]: sanitize_digits('123ASDF')
    Out[2]: '123'

validate_cpf
------------

Validates CPF code and return the original number

Ps: doesn't matter if you use a masked number or not

Usage:

.. code-block:: python

    In[0]: from django_models.utils import validate_cpf
    In[1]: validate_cnpj('01212312312')   # Invalid
    Out[1]: False
    In[2]: validate_cpf('062.265.326-10') # Valid
    Out[2]: '062.265.326-10'

validate_cnpj
-------------

Validates CNPJ code and return the original number

Ps: doesn't matter if you use a masked number or not

Usage:

.. code-block:: python

    In[0]: from django_models.utils import validate_cnpj
    In[1]: validate_cnpj('12345123/000000')      # Invalid
    Out[1]: False
    In[2]: validate_cnpj('61.553.678/0001-96')   # Valid
    Out[2]: '61.553.678/0001-96'
