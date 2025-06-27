#!/usr/bin/env python
# encoding: utf-8
"""
Django Models Library

A comprehensive Django extension library that provides useful abstract models,
custom fields, forms, validators, and utilities to help you build Django
applications with less boilerplate code and more functionality.

This library includes:
- Abstract models for common patterns (timestamps, soft delete, UUID primary keys, etc.)
- Custom fields for Brazilian documents and other specialized use cases
- Form fields with built-in validation
- Signal-based models for custom event handling
- Utility functions for string manipulation and code generation
"""

from typing import List

default_app_config = "django_models.apps.DjangoModelsConfig"

from .version import __version__  # noqa
from . import utils  # noqa
from . import fields  # noqa
from . import forms  # noqa
from . import validators  # noqa

__all__: List[str] = ["__version__", "utils", "fields", "forms", "validators"]
