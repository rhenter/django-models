Documentation
=============

Update or Add New
-----------------

To add new or update documentation, you must add or change existing files in RST format, located at ``docs_src/source``

.. note::
  If you added a new file, make sure you add the reference in the directory ``docs_src/source/index.rst``


Update the translation
----------------------

Today we have 2 translations, being ``en`` (english) and ``pt_BR`` Portuguese, if you want to add one more,
just add the prefix of the language that will be generated or updated in located in ``docs_src/source/locale/``

* Generate the .po files to update

.. code-block:: bash

    $ cd docs_src
    $ make gettext
    $ sphinx-intl update -p build/gettext -l pt_BR -l en


* Update the .po files in ``docs_src/source/locale/< LANGUAGE prefix >/LC_MESSAGES/``

Example:

.. code-block:: text

    #: ../../source/index.rst:28
    msgid "User Guide"
    msgstr "Guia do Usuário"


.. note::
  The .mo file will be generated when you generate the HTML files

Generating the documentation
----------------------------

The project uses GitHub Pages to host the documentation files, so all HTML files must be located in /doc

.. code-block:: bash

    $ cd docs_src
    $ sphinx-build -b html source ../docs/en -D language='en'
    $ sphinx-build -b html source ../docs/pt-br -D language='pt_BR'
