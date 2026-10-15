Changelog
=========
1.1.0
~~~~~

- Added support for Python 3.13 and 3.14
- Added support for Django 6.0
- Added a GitHub Actions test matrix for supported Python and Django versions
- Fixed signal handlers silently suppressing exceptions
- Fixed the test and release Makefile targets
- Fixed test project files being included in the wheel
- Modernized package builds with the standard Python build frontend

1.0
~~~

- Fixed Django 5 compatibility issues
- Updated requirements to Django 5.0+
- Fixed broken tests with pytest
- Updated documentation

0.5.1
~~~~~

- Expose/Export SoftDeleteSignalModel Model

0.5.0
~~~~~

- Move post_save to outside of the transaction on the Signal Model

0.4.1
~~~~~

- Corrected import / inherited model class

0.4.0
~~~~~

- Change Default code size to 8 on CodeModel

0.3.0
~~~~~

- Use new documentation on GitHub Pages

0.2.1
~~~~~

- Fix typo

0.2.0
~~~~~

- Update documentation
- Translate the documentation to Portuguese

0.1.0
~~~~~

- Start a new from Project from Django Stuff
