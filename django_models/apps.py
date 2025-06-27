from django.apps import AppConfig


class DjangoModelsConfig(AppConfig):
    """
    Django app configuration for django_models package.

    This configuration class is required for Django to properly
    recognize and load the django_models package as a Django app.
    """

    default_auto_field = "django.db.models.BigAutoField"
    name = "django_models"
    verbose_name = "Django Models Library"
