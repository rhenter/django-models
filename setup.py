import os
import re
from typing import List

from setuptools import setup, find_packages, Command

here = os.path.abspath(os.path.dirname(__file__))


def get_version_from_changes() -> str:
    changes_path = os.path.join(here, "CHANGES.rst")
    version_pattern = re.compile(r"^(?P<version>[0-9]+\.[0-9]+(?:\.[0-9]+)?)")

    with open(changes_path, encoding="utf-8") as changes_file:
        for line in changes_file:
            match = version_pattern.match(line)
            if match:
                return match.group("version")

    raise ValueError("No version found in CHANGES.rst")


version = get_version_from_changes()


# Save last Version
def save_version() -> None:
    """Save the current version to the version.py file."""
    version_path = os.path.join(here, "django_models/version.py")

    with open(version_path) as version_file_read:
        content_file = version_file_read.read()

    VSRE = r"^__version__ = ['\"]([^'\"]*)['\"]"
    mo = re.search(VSRE, content_file, re.M)
    if mo is None:
        raise ValueError("Version pattern not found in version.py")
    current_version = mo.group(1)

    content_file = content_file.replace(current_version, "{}".format(version))

    with open(version_path, 'w') as version_file_write:
        version_file_write.write(content_file)


save_version()


# Get the long description
with open(os.path.join(here, 'README.rst'), encoding='utf-8') as f:
    long_description = f.read()

# Get changelog
with open(os.path.join(here, 'CHANGES.rst'), encoding='utf-8') as f:
    changelog = f.read()

with open(os.path.join(here, 'requirements.txt'), encoding='utf-8') as f:
    install_requires = [line for line in f.readlines() if not line.startswith('#')]


class VersionCommand(Command):
    """Custom command to print the library version."""
    description = 'print library version'
    user_options: List = []

    def initialize_options(self) -> None:
        """Initialize command options."""
        pass

    def finalize_options(self) -> None:
        """Finalize command options."""
        pass

    def run(self) -> None:
        """Run the version command."""
        print(version)


setup(
    author='Rafael Henter',
    author_email='rafael@henter.com.br',
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Framework :: Django',
        'Framework :: Django :: 5.0',
        'Framework :: Django :: 5.1',
        'Framework :: Django :: 5.2',
        'Framework :: Django :: 6.0',
        'Intended Audience :: Developers',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
        'Programming Language :: Python :: 3.12',
        'Programming Language :: Python :: 3.13',
        'Programming Language :: Python :: 3.14',
        'Topic :: Software Development :: Libraries',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Typing :: Typed',
    ],
    cmdclass={'version': VersionCommand},
    description='Library with several useful Models for Django to help you make your Models smart or with less code',
    install_requires=install_requires,
    keywords='models tools django signal',
    license='MIT',
    long_description=long_description,
    long_description_content_type='text/x-rst',
    name='django-models',
    packages=find_packages(exclude=['docs', 'tests*', 'test-django-project*']),
    python_requires='>=3.10',
    url='https://github.com/rhenter/django-models',
    version=version,
)
